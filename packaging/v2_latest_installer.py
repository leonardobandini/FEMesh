# SPDX-License-Identifier: GPL-2.0-or-later
"""Attach a fixed-name installer ZIP to the published latest V2 release.

Permanent public URL:
https://github.com/leonardobandini/sap2000-quad-mesher-updates/releases/latest/download/Sap2000QuadMesher-latest.zip

Run after publishing the versioned ZIP and before announcing the release in
either update feed. Does not replace an existing asset or alter an older release.
"""
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REPOSITORY = 'leonardobandini/sap2000-quad-mesher-updates'
ALIAS = 'Sap2000QuadMesher-latest.zip'
URL = f'https://github.com/{REPOSITORY}/releases/latest/download/{ALIAS}'


def gh(*args):
    return subprocess.run(['gh', *args], check=True, capture_output=True, text=True).stdout


def ensure_latest_installer(version):
    tag = 'v' + version
    named = f'Sap2000QuadMesher-{version}.zip'
    source = ROOT / 'artifacts' / named
    checksum_file = ROOT / 'artifacts' / (named + '.sha256')
    expected = hashlib.sha256(source.read_bytes()).hexdigest()
    if tuple(checksum_file.read_text(encoding='ascii').split()) != (expected, named):
        raise ValueError('Local installer ZIP does not match its checksum')
    latest = json.loads(gh('api', f'repos/{REPOSITORY}/releases/latest'))
    if latest['tag_name'] != tag or latest['draft'] or latest['prerelease']:
        raise ValueError('The requested V2 release is not the published latest release')
    assets = {asset['name']: asset for asset in latest['assets']}
    digest = 'sha256:' + expected
    if named not in assets or assets[named]['digest'] != digest:
        raise ValueError('The public versioned ZIP differs from the local installer')
    branded_name = f'FEMesher-{version}.zip'
    aliases = [ALIAS]
    if tuple(map(int, version.split('.'))) >= (2, 0, 57):
        if (ROOT / 'artifacts' / branded_name).read_bytes() != source.read_bytes() or \
           branded_name not in assets or assets[branded_name]['digest'] != digest:
            raise ValueError('The branded versioned ZIP differs from the legacy-compatible installer')
        aliases.append('FEMesher-latest.zip')
    if tuple(map(int, version.split('.'))) >= (2, 0, 63):
        public_name = f'FEMesh-{version}.zip'
        if (ROOT / 'artifacts' / public_name).read_bytes() != source.read_bytes() or \
           public_name not in assets or assets[public_name]['digest'] != digest:
            raise ValueError('The public FEMesh ZIP differs from the compatible installer')
        aliases.append('FEMesh-latest.zip')
    parent = Path(tempfile.gettempdir()) / 'opencode'
    if not parent.is_dir():
        raise FileNotFoundError('Approved temporary directory is missing: ' + str(parent))
    with tempfile.TemporaryDirectory(prefix='sqm-latest-installer-', dir=parent) as folder:
        for name in aliases:
            if name in assets:
                if assets[name]['digest'] != digest or assets[name]['size'] != source.stat().st_size:
                    raise ValueError('The latest release already has a different fixed-name installer: ' + name)
                continue
            alias = Path(folder) / name
            shutil.copyfile(source, alias)
            if hashlib.sha256(alias.read_bytes()).hexdigest() != expected:
                raise IOError('Staged fixed-name installer differs from the release ZIP')
            gh('release', 'upload', tag, str(alias), '-R', REPOSITORY)
    published = json.loads(gh('api', f'repos/{REPOSITORY}/releases/latest'))
    current = {asset['name']: asset for asset in published['assets']}
    if published['tag_name'] != tag or any(name not in current or
        current[name]['digest'] != digest or current[name]['size'] != source.stat().st_size for name in aliases):
        raise RuntimeError('The fixed URL is not backed by the verified installer ZIP')
    print(f'LATEST_INSTALLER=PUBLISHED VERSION={version} SHA256={expected} URL={URL}')
    return URL


if __name__ == '__main__':
    manifest = json.loads((ROOT / 'updates' / 'manifest-v2.json').read_text(encoding='utf-8'))
    ensure_latest_installer(manifest['version'])
