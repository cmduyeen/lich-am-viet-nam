"""Standard-library-only freshness check; safe before installing dependencies."""
import argparse
import hashlib
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_FILE = '.build-state.json'
SCHEMA = 1

def current_year():
    return datetime.now(timezone(timedelta(hours=7))).year

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def fingerprint(root=ROOT, year=None, custom_configs=(), start=None, end=None, split=False):
    root=Path(root)
    files=sorted([*root.joinpath('src').glob('*.py'), *root.joinpath('src').glob('*.json'),
                  root/'main.py', root/'generate_all.py', root/'requirements.txt'])
    inputs={str(p.relative_to(root)).replace('\\','/'):digest(p.read_text(encoding='utf-8').encode('utf-8')) for p in files}
    configs=[digest(Path(p).read_text(encoding='utf-8').encode('utf-8')) for p in custom_configs]
    data=dict(schema=SCHEMA, year=current_year() if year is None else year, inputs=inputs,
              configs=configs, start=start, end=end, split=split)
    return digest(json.dumps(data,sort_keys=True).encode('utf-8'))

def is_current(output, expected):
    output=Path(output)
    try:
        state=json.loads((output/STATE_FILE).read_text(encoding='utf-8'))
        if state.get('schema')!=SCHEMA or state.get('fingerprint')!=expected:return False
        hashes=state.get('files')
        if not isinstance(hashes,dict) or 'index.json' not in hashes:return False
        for name,checksum in hashes.items():
            path=output/name
            if Path(name).name!=name or path.is_symlink() or not path.is_file():return False
            if digest(path.read_bytes())!=checksum:return False
        inventory=json.loads((output/'index.json').read_text(encoding='utf-8'))
        if not inventory:return False
        return all(entry['file'] in hashes and entry['sha256']==hashes[entry['file']] for entry in inventory)
    except (OSError,ValueError,KeyError,TypeError,AttributeError):
        return False

def write_state(staging, expected):
    staging=Path(staging)
    hashes={p.name:digest(p.read_bytes()) for p in sorted(staging.iterdir()) if p.is_file() and p.name!=STATE_FILE}
    (staging/STATE_FILE).write_text(json.dumps(dict(schema=SCHEMA,fingerprint=expected,files=hashes),indent=2)+'\n',encoding='utf-8',newline='\n')

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check',action='store_true',required=True)
    p.add_argument('--output-dir',type=Path,default=ROOT/'output')
    p.add_argument('--custom-config',type=Path,action='append',default=[])
    p.add_argument('--start',type=int);p.add_argument('--end',type=int)
    p.add_argument('--split',action='store_true')
    args=p.parse_args(argv)
    try:
        expected=fingerprint(custom_configs=args.custom_config,start=args.start,end=args.end,split=args.split)
        fresh=is_current(args.output_dir,expected)
    except (OSError,ValueError):fresh=False
    print('Up to date: no generation needed' if fresh else 'Build required')
    return 0 if fresh else 1

if __name__=='__main__':raise SystemExit(main())
