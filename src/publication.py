"""Publish only the standard public calendar filenames, never personal calendars."""

import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .files import atomic_write

PUBLIC_FILENAME = re.compile(
    r'(?:update-status\.json|viet_lunar(?:_en)?_'
    r'(?:latest\.ics|\d{4}(?:_\d{4})?\.ics|yearly_\d{4}_\d{4}\.zip))'
)


def public_paths(root):
    root = Path(root)
    tracked = subprocess.run(
        ['git', 'ls-files', '-z', '--', 'output/'], cwd=root,
        check=True, capture_output=True,
    ).stdout.decode('utf-8').split('\0')
    candidates = {Path(name).name for name in tracked if name}
    output = root / 'output'
    if output.is_symlink():
        raise ValueError('Public output directory must not be a symlink')
    if output.exists():
        candidates.update(path.name for path in output.iterdir())
    paths = []
    for name in sorted(candidates):
        if not PUBLIC_FILENAME.fullmatch(name):
            continue
        path = output / name
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError('Public exports must be regular files')
        paths.append('output/' + name)
    return paths


def stage_public_outputs(root):
    paths = public_paths(root)
    if paths:
        subprocess.run(['git', 'add', '--', *paths], cwd=root, check=True)


def record_refresh(root):
    raw = json.dumps({
        'updated_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'languages': ['vi', 'en'],
    }, indent=2) + '\n'
    atomic_write(Path(root) / 'output/update-status.json', raw.encode('utf-8'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--stage', action='store_true')
    group.add_argument('--record', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    if args.stage:
        stage_public_outputs(root)
    else:
        record_refresh(root)


if __name__ == '__main__':
    main()
