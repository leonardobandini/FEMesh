# SPDX-License-Identifier: GPL-2.0-or-later
"""Publish only the V2 update manifest after the V2 ZIP is verified online.

Never modify the V1 manifest or remove existing releases.
"""
import base64
import hashlib
import json
import subprocess
from pathlib import Path

from v2_latest_installer import ensure_latest_installer

ROOT = Path(__file__).resolve().parent.parent
REPO = 'leonardobandini/sap2000-quad-mesher-updates'
TARGET = f'repos/{REPO}/contents/manifest-v2.json'


def gh(*arguments):
    result = subprocess.run(['gh', *arguments], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def main():
    path = ROOT / 'updates' / 'manifest-v2.json'
    manifest = json.loads(path.read_text(encoding='utf-8'))
    version = manifest['version']
    expected_tag = f'v{version}'
    filename = f'Sap2000QuadMesher-{version}.zip'
    assert version.startswith('2.') and manifest['schemaVersion'] == 1
    assert manifest['releaseUrl'] == f'https://github.com/{REPO}/releases/tag/{expected_tag}'
    assert manifest['downloadUrl'] == f'https://github.com/{REPO}/releases/download/{expected_tag}/{filename}'
    zip_path = ROOT / 'artifacts' / filename
    checksum = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    checked, checked_name = (ROOT / 'artifacts' / (filename + '.sha256')).read_text(encoding='ascii').split()
    assert (checked, checked_name) == (checksum, filename)
    release = gh('api', f'repos/{REPO}/releases/tags/{expected_tag}')
    if release['draft'] or not any(asset['name'] == filename and asset['digest'] == 'sha256:' + checksum
                                    for asset in release['assets']):
        raise ValueError('The release ZIP is not published with the local SHA-256')
    # The same verified installer is also published under a stable asset name
    # before a new V2 release is offered by the update feed.
    ensure_latest_installer(version)
    try:
        previous = gh('api', TARGET)
    except subprocess.CalledProcessError as error:
        if 'HTTP 404' not in error.stderr:
            raise
        previous = None
    if previous:
        old = json.loads(base64.b64decode(previous['content']))
        if old == manifest:
            print('V2_FEED=UNCHANGED VERSION=' + version)
            return
        if not old['version'].startswith('2.') or tuple(map(int, version.split('.'))) <= tuple(map(int, old['version'].split('.'))):
            raise ValueError('Refusing a V2 feed rollback or cross-channel update')
    content = base64.b64encode(path.read_bytes()).decode('ascii')
    args = ['api', '-X', 'PUT', TARGET, '-f', f'message=Publish V2 update manifest {expected_tag}',
            '-f', f'content={content}', '-f', 'branch=main']
    if previous:
        args.extend(['-f', 'sha=' + previous['sha']])
    gh(*args)
    remote = gh('api', TARGET)
    if base64.b64decode(remote['content']) != path.read_bytes():
        raise RuntimeError('Published V2 feed differs from local release manifest')
    print('V2_FEED=PUBLISHED VERSION=' + version)


if __name__ == '__main__':
    main()
