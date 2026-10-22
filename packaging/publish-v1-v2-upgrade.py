# SPDX-License-Identifier: GPL-2.0-or-later
"""Offer a verified V2 ZIP to the existing V1 update channel without pruning history."""
import base64
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = 'leonardobandini/sap2000-quad-mesher-updates'
TARGET = f'repos/{REPO}/contents/manifest.json'


def gh(*args):
    return json.loads(subprocess.run(['gh', *args], capture_output=True, text=True, check=True).stdout)


def main():
    manifest_path = ROOT / 'updates' / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    version = manifest['version']
    tag = f'v{version}'
    filename = f'Sap2000QuadMesher-{version}.zip'
    assert version.startswith('2.') and manifest['schemaVersion'] == 1
    assert manifest['releaseUrl'] == f'https://github.com/{REPO}/releases/tag/{tag}'
    assert manifest['downloadUrl'] == f'https://github.com/{REPO}/releases/download/{tag}/{filename}'
    path = ROOT / 'artifacts' / filename
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    expected, basename = (ROOT / 'artifacts' / (filename + '.sha256')).read_text(encoding='ascii').split()
    assert (expected, basename) == (sha, filename)
    release = gh('api', f'repos/{REPO}/releases/tags/{tag}')
    if release['draft'] or not any(asset['name'] == filename and asset['digest'] == 'sha256:' + sha
                                   for asset in release['assets']):
        raise ValueError('The V2 ZIP is not published and digest-verified')
    archived = gh('api', f'repos/{REPO}/contents/{tag}/{filename[:-4]}-source.zip?ref=source-archive')
    if archived.get('type') != 'file':
        raise ValueError('Corresponding GPL sources are not archived before V1 migration')
    previous = gh('api', TARGET)
    old = json.loads(base64.b64decode(previous['content']))
    if old == manifest:
        print('V1_UPGRADE_FEED=UNCHANGED VERSION=' + version)
        return
    if not old['version'].startswith(('1.', '2.')) or \
            tuple(map(int, old['version'].split('.'))) >= tuple(map(int, version.split('.'))):
        raise ValueError('Unexpected upgrade channel: refusing to overwrite a foreign/newer feed')
    gh('api', '-X', 'PUT', TARGET, '-f', f'message=Offer V2 {tag} to V1 users',
       '-f', 'content=' + base64.b64encode(manifest_path.read_bytes()).decode('ascii'),
       '-f', 'branch=main', '-f', 'sha=' + previous['sha'])
    final = gh('api', TARGET)
    if base64.b64decode(final['content']) != manifest_path.read_bytes():
        raise RuntimeError('Remote V1 feed differs from the verified local V2 release URL')
    print('V1_UPGRADE_FEED=PUBLISHED VERSION=' + version)


if __name__ == '__main__':
    main()
