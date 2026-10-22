# Copyright (C) 2026 Leonardo Bandini
# SPDX-License-Identifier: GPL-2.0-or-later
"""Publish a verified public release, then keep only its public release and tag."""

import argparse
import base64
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REPOSITORY = "leonardobandini/sap2000-quad-mesher-updates"
RELEASES = f"repos/{REPOSITORY}/releases"
ARCHIVE_BRANCH = "source-archive"
TAG_PATTERN = re.compile(r"v\d+\.\d+\.\d+\Z")


def gh(*arguments):
    for attempt in range(4):
        command = ["gh", *map(str, arguments)]
        result = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, check=False)
        if result.returncode == 0:
            return result.stdout
        if attempt < 3 and ("error connecting" in result.stderr.lower() or
                            "could not resolve host" in result.stderr.lower()):
            time.sleep(3)
            continue
        raise RuntimeError(f"{' '.join(command)} failed: {result.stderr.strip()}")


def api(path, *arguments):
    return json.loads(gh("api", path, *arguments))


def git(*arguments, cwd=None):
    for attempt in range(4):
        command = ["git", *map(str, arguments)]
        result = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, check=False)
        if result.returncode == 0:
            return result.stdout.strip()
        if attempt < 3 and "could not resolve host" in result.stderr.lower():
            time.sleep(3)
            continue
        raise RuntimeError(f"{' '.join(command)} failed: {result.stderr.strip()}")


def assets_for(version):
    base = ROOT / "artifacts"
    names = [f"Sap2000QuadMesher-{version}.zip",
             f"Sap2000QuadMesher-{version}.zip.sha256",
             f"Sap2000QuadMesher-{version}-source.zip",
             f"Sap2000QuadMesher-{version}-source.zip.sha256",
             "gmsh-4.15.2-source.tgz", "gmsh-4.15.2-source.tgz.sha256"]
    if tuple(map(int, version.split('.'))) >= (2, 0, 57):
        names.extend((f"FEMesher-{version}.zip", f"FEMesher-{version}.zip.sha256"))
    if tuple(map(int, version.split('.'))) >= (2, 0, 63):
        names.extend((f"FEMesh-{version}.zip", f"FEMesh-{version}.zip.sha256"))
    files = {name: base / name for name in names}
    for name, path in files.items():
        if not path.is_file():
            raise FileNotFoundError(path)
        if name.endswith(".sha256"):
            continue
        expected, filename = (base / (name + ".sha256")).read_text(encoding="ascii").split()
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if filename != name or actual != expected:
            raise RuntimeError(f"Checksum mismatch: {path}")
    if tuple(map(int, version.split('.'))) >= (2, 0, 57) and \
       hashlib.sha256(files[f"FEMesher-{version}.zip"].read_bytes()).digest() != \
       hashlib.sha256(files[f"Sap2000QuadMesher-{version}.zip"].read_bytes()).digest():
        raise RuntimeError("Legacy and FEMesher ZIPs must have the same content")
    if tuple(map(int, version.split('.'))) >= (2, 0, 63) and \
       hashlib.sha256(files[f"FEMesh-{version}.zip"].read_bytes()).digest() != \
       hashlib.sha256(files[f"Sap2000QuadMesher-{version}.zip"].read_bytes()).digest():
        raise RuntimeError("Legacy and FEMesh ZIPs must have the same content")
    return files


def release(tag):
    try:
        return api(f"{RELEASES}/tags/{tag}")
    except RuntimeError as error:
        if "HTTP 404" not in str(error) and "release not found" not in str(error).lower():
            raise
        return None


def verify_release(record, tag, files):
    if record is None or record["tag_name"] != tag:
        raise RuntimeError("The new release is not available under the requested tag")
    actual = {asset["name"]: asset for asset in record["assets"]}
    if set(actual) != set(files):
        raise RuntimeError(f"Release asset set differs from expected: {sorted(actual)}")
    for name, path in files.items():
        digest = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        if actual[name]["digest"] != digest:
            raise RuntimeError(f"Remote release asset does not match local file: {name}")


def publish_manifest(manifest, dry_run):
    path = f"repos/{REPOSITORY}/contents/manifest.json"
    published = api(path)
    current = base64.b64decode(published["content"])
    wanted = json.dumps(manifest, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
    if json.loads(current) == manifest:
        print("Public update manifest already points to " + manifest["version"])
        return
    if dry_run:
        print("Would update the public update manifest to " + manifest["version"])
        return
    payload = {"message": "Publish update manifest v" + manifest["version"],
               "content": base64.b64encode(wanted).decode("ascii"),
               "sha": published["sha"], "branch": "main"}
    temp_root = Path(tempfile.gettempdir()) / "opencode"
    if not temp_root.is_dir():
        raise RuntimeError("Approved temporary directory is missing: " + str(temp_root))
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".json",
                                     prefix="sqm-manifest-", dir=temp_root, delete=False) as stream:
        json.dump(payload, stream)
        input_path = Path(stream.name)
    try:
        gh("api", "-X", "PUT", path, "--input", input_path)
    finally:
        input_path.unlink(missing_ok=True)
    if json.loads(base64.b64decode(api(path)["content"])) != manifest:
        raise RuntimeError("Public manifest was not updated; older releases were left intact")
    print("Published manifest for " + manifest["version"])


def list_releases():
    items = api(RELEASES + "?per_page=100")
    if len(items) >= 100:
        raise RuntimeError("Release listing needs pagination; refusing to delete anything")
    return items


def archived_source_paths(tag):
    version = tag[1:]
    source_name = f"Sap2000QuadMesher-{version}-source.zip"
    return (f"{tag}/{source_name}", f"{tag}/{source_name}.sha256",
            "gmsh-4.15.2-source.tgz", "gmsh-4.15.2-source.tgz.sha256")


def archive_tree():
    tree = api(f"repos/{REPOSITORY}/git/trees/{ARCHIVE_BRANCH}?recursive=1")
    if tree.get("truncated"):
        raise RuntimeError("Source archive listing is incomplete; refusing to prune releases")
    return {item["path"]: item for item in tree["tree"] if item["type"] == "blob"}


def archive_sources(tag, files, dry_run):
    version = tag[1:]
    expected = archived_source_paths(tag)
    existing = archive_tree()
    source_name = f"Sap2000QuadMesher-{version}-source.zip"
    local_files = (files[source_name], files[source_name + ".sha256"],
                   files["gmsh-4.15.2-source.tgz"], files["gmsh-4.15.2-source.tgz.sha256"])
    for relative, local in zip(expected, local_files):
        if relative in existing and existing[relative]["sha"] != git("hash-object", local):
            raise RuntimeError("Published historical source differs from local asset: " + relative)
    missing = [name for name in expected if name not in existing]
    if not missing:
        print("Stable source archive already contains " + tag)
        return
    if dry_run:
        print("Would preserve GPL source in the public source-archive branch: " + ", ".join(missing))
        return

    temp_root = Path(tempfile.gettempdir()) / "opencode"
    if not temp_root.is_dir():
        raise RuntimeError("Approved temporary directory is missing: " + str(temp_root))
    with tempfile.TemporaryDirectory(prefix="sqm-source-archive-", dir=temp_root) as folder:
        checkout = Path(folder) / "checkout"
        git("clone", "--depth", "1", "--single-branch", "--branch", ARCHIVE_BRANCH,
            f"https://github.com/{REPOSITORY}.git", checkout)
        for relative, local in zip(expected, local_files):
            target = checkout / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                if hashlib.sha256(target.read_bytes()).digest() != hashlib.sha256(local.read_bytes()).digest():
                    raise RuntimeError("Archived source differs from release source: " + relative)
            else:
                shutil.copyfile(local, target)
        index = checkout / "README.md"
        link = f"v{version}/{source_name}"
        if link not in index.read_text(encoding="utf-8"):
            with index.open("a", encoding="utf-8") as stream:
                stream.write(f"\n- [v{version}: corresponding source]({link}) and "
                             f"[SHA-256]({link}.sha256)\n")
        git("add", "README.md", *missing, cwd=checkout)
        if git("status", "--porcelain", cwd=checkout):
            git("commit", "-m", f"Archive corresponding source for {tag}", cwd=checkout)
            git("push", "origin", ARCHIVE_BRANCH, cwd=checkout)
        revision = git("rev-parse", "HEAD", cwd=checkout)
        remote = git("ls-remote", "origin", f"refs/heads/{ARCHIVE_BRANCH}", cwd=checkout)
        if not remote.startswith(revision + "\t"):
            raise RuntimeError("The historical source archive was not published")

    published = archive_tree()
    if not all(name in published for name in expected):
        raise RuntimeError("Source archive is not publicly indexed; older releases remain available")
    url = (f"https://raw.githubusercontent.com/{REPOSITORY}/{ARCHIVE_BRANCH}/"
           f"{tag}/{source_name}")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=15) as response:
                if response.status == 200:
                    print("Stable corresponding source: " + url)
                    return
        except OSError:
            if attempt == 2:
                raise
            time.sleep(2)
    raise RuntimeError("The historical source URL is not publicly accessible")


def prune(keep, keep_id, dry_run):
    records = list_releases()
    if not any(item["id"] == keep_id and not item["draft"] for item in records):
        raise RuntimeError("Verified public release missing; refusing to delete anything")
    old = [item for item in records if item["id"] != keep_id]
    if any(not TAG_PATTERN.fullmatch(item["tag_name"]) for item in old):
        raise RuntimeError("Unexpected release tag; refusing to delete anything")
    preserved = archive_tree()
    for item in old:
        version = tuple(map(int, item["tag_name"][1:].split(".")))
        if version >= (1, 0, 78) and not all(name in preserved for name in archived_source_paths(item["tag_name"])):
            raise RuntimeError("Corresponding source missing from permanent archive: " + item["tag_name"])
    for item in old:
        print(f"{'Would remove' if dry_run else 'Removing'} old public release "
              f"{item['tag_name']} (id={item['id']}, draft={item['draft']})")
        if not dry_run:
            gh("api", "-X", "DELETE", f"{RELEASES}/{item['id']}")

    refs = api(f"repos/{REPOSITORY}/git/matching-refs/tags")
    for entry in refs:
        name = entry["ref"].removeprefix("refs/tags/")
        if name == keep or not TAG_PATTERN.fullmatch(name):
            continue
        print(f"{'Would remove' if dry_run else 'Removing'} old public tag {name}")
        if not dry_run:
            gh("api", "-X", "DELETE", f"repos/{REPOSITORY}/git/refs/tags/{name}")

    if not dry_run:
        remaining = list_releases()
        tags = {entry["ref"] for entry in api(f"repos/{REPOSITORY}/git/matching-refs/tags")
                if TAG_PATTERN.fullmatch(entry["ref"].removeprefix("refs/tags/"))}
        if len(remaining) != 1 or remaining[0]["id"] != keep_id or tags != {"refs/tags/" + keep}:
            raise RuntimeError("Public release cleanup is incomplete")
        print("Public repository now contains only release and tag " + keep)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag", help="Version tag, e.g. v1.0.78")
    parser.add_argument("--title", default="")
    parser.add_argument("--notes", default="")
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    if not TAG_PATTERN.fullmatch(arguments.tag):
        parser.error("Expected a version tag such as v1.0.78")

    version = arguments.tag[1:]
    manifest = json.loads((ROOT / "updates" / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("version") != version or manifest.get("schemaVersion") != 1 or \
       manifest.get("releaseUrl") != f"https://github.com/{REPOSITORY}/releases/tag/{arguments.tag}" or \
       manifest.get("downloadUrl") != (f"https://github.com/{REPOSITORY}/releases/download/"
                                       f"{arguments.tag}/Sap2000QuadMesher-{version}.zip"):
        raise RuntimeError("The local update manifest does not match the requested release")
    files = assets_for(version)
    record = release(arguments.tag)
    if record is None and arguments.dry_run:
        print(f"Would create release {arguments.tag} with {len(files)} verified assets")
        return
    if record is None:
        if not arguments.title or not arguments.notes:
            raise RuntimeError("--title and --notes are required for a new release")
        gh("release", "create", arguments.tag, *files.values(), "--repo", REPOSITORY,
           "--title", arguments.title, "--notes", arguments.notes)
        record = release(arguments.tag)
    elif set(asset["name"] for asset in record["assets"]) != set(files):
        published_names = {asset["name"] for asset in record["assets"]}
        if not published_names.issubset(files):
            raise RuntimeError("The existing release contains unexpected assets")
        missing = [name for name in files if name not in published_names]
        if arguments.dry_run:
            print("Would upload missing assets: " + ", ".join(missing))
            return
        for name in missing:
            gh("release", "upload", arguments.tag, files[name], "--repo", REPOSITORY)
        record = release(arguments.tag)
    verify_release(record, arguments.tag, files)
    if record["draft"] and not arguments.dry_run:
        gh("release", "edit", arguments.tag, "--repo", REPOSITORY, "--draft=false")
        record = release(arguments.tag)
    if record["draft"]:
        raise RuntimeError("The new release is still a draft; older releases were left intact")
    archive_sources(arguments.tag, files, arguments.dry_run)
    publish_manifest(manifest, arguments.dry_run)
    if not arguments.dry_run and json.loads(base64.b64decode(
            api(f"repos/{REPOSITORY}/contents/manifest.json")["content"])) != manifest:
        raise RuntimeError("Manifest mismatch; older releases were left intact")
    prune(arguments.tag, record["id"], arguments.dry_run)


if __name__ == "__main__":
    main()
