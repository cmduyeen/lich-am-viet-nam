"""Wire validation, stable revisions and atomic file replacement."""
from copy import deepcopy
from datetime import date, datetime, timezone
import os
import re
from pathlib import Path
import tempfile
import zipfile
from icalendar import Calendar, Event

_REVISION_FIELDS={'DTSTAMP','LAST-MODIFIED','SEQUENCE','CREATED'}


def _fingerprint(event):
    value=Event()
    for key,prop in event.items():
        if key not in _REVISION_FIELDS:
            value[key]=prop
    return value.to_ical()


def reconcile(calendar, previous=None):
    """Keep unmodified events byte-stable; update changed events under the same UID."""
    result=deepcopy(calendar)
    prior={}
    if previous and Path(previous).exists():
        old=Calendar.from_ical(Path(previous).read_bytes())
        prior={str(e['uid']):e for e in old.walk('VEVENT')}
    now=datetime.now(timezone.utc).replace(microsecond=0)
    for event in result.walk('VEVENT'):
        old=prior.get(str(event['uid']))
        if old is None: continue
        try:
            old_stamp=old.decoded('dtstamp')
            valid_stamp=isinstance(old_stamp,datetime) and old_stamp.tzinfo is not None and old_stamp.utcoffset().total_seconds()==0
        except (ValueError,KeyError):
            valid_stamp=False
        if valid_stamp and _fingerprint(old)==_fingerprint(event):
            for key in _REVISION_FIELDS:
                event.pop(key,None)
                if key in old: event[key]=old[key]
        else:
            event.pop('DTSTAMP',None)
            event.pop('LAST-MODIFIED',None)
            event.add('DTSTAMP',now)
            event.add('LAST-MODIFIED',now)
            event['SEQUENCE']=int(old.get('SEQUENCE',0))+1
    return result


def validate_bytes(raw):
    if b'\n' in raw.replace(b'\r\n',b''):
        raise ValueError('ICS must use CRLF line endings')
    if any(len(line)>75 for line in raw.split(b'\r\n')):
        raise ValueError('ICS lines must be folded within 75 bytes')
    calendar=Calendar.from_ical(raw)
    seen=set()
    for event in calendar.walk('VEVENT'):
        uid=str(event['uid'])
        if uid in seen: raise ValueError(f'Duplicate UID: {uid}')
        seen.add(uid)
        first,last=event.decoded('dtstart'),event.decoded('dtend')
        if type(first) is not date or type(last) is not date or (last-first).days!=1:
            raise ValueError('Events must have one-day DATE boundaries')
        if not str(event['summary']): raise ValueError('Empty event summary')
        stamp=event.decoded('dtstamp')
        if not isinstance(stamp,datetime) or stamp.tzinfo is None or stamp.utcoffset().total_seconds()!=0:
            raise ValueError('DTSTAMP must be a valid UTC datetime')
    return calendar


def atomic_write(path,raw):
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() and path.read_bytes()==raw: return False
    with tempfile.NamedTemporaryFile(dir=path.parent,delete=False) as file:
        temp=Path(file.name)
        file.write(raw)
    try: os.replace(temp,path)
    finally: temp.unlink(missing_ok=True)
    return True


def write_calendar(calendar,path,previous=None,*,reconciled=False):
    value=calendar if reconciled else reconcile(calendar,previous or path)
    raw=value.to_ical()
    validate_bytes(raw)
    atomic_write(path,raw)
    return value


def create_zip(files,target):
    """Fixed ZIP metadata avoids a different archive on each generation."""
    target=Path(target)
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(map(Path,files)):
            info=zipfile.ZipInfo(path.name,(2000,1,1,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(info,path.read_bytes())
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None: raise ValueError('Corrupt ZIP archive')


def obsolete_exports(output, staging, manifest):
    """Prune only generated dated exports for active, non-custom feed prefixes.

    Latest URLs, unrelated files and custom snapshots are never selected here.
    Save optional historical snapshots outside output/ to retain them permanently.
    """
    output,staging=Path(output),Path(staging)
    if not output.exists(): return []
    keep={file.name for file in staging.iterdir()}
    prefixes=[entry['file'].removesuffix('_latest.ics') for entry in manifest
              if entry['file'].endswith('_latest.ics') and '_custom_' not in entry['file'] and not entry['file'].startswith('custom_')]
    patterns=[re.compile(re.escape(prefix)+r'_(?:\d{4}(?:_\d{4})?\.ics|yearly_\d{4}_\d{4}\.zip)$')
              for prefix in prefixes]
    result=[]
    for file in output.iterdir():
        if file.is_file() and not file.is_symlink() and file.name not in keep:
            if any(pattern.fullmatch(file.name) for pattern in patterns):
                result.append(file.name)
    return sorted(result)


def publish_staged(staging,output,obsolete=()):
    """Publish validated files and retire managed exports; rollback on failure."""
    staging,output=Path(staging),Path(output)
    output.mkdir(parents=True,exist_ok=True)
    root=output.resolve()
    files=sorted(staging.iterdir(),key=lambda p:p.name)
    operations=[(source.name,source.read_bytes()) for source in files if source.name!='index.json']
    operations.extend((name,None) for name in obsolete)
    operations.extend((source.name,source.read_bytes()) for source in files if source.name=='index.json')
    for name,_ in operations:
        destination=output/name
        if Path(name).name!=name or destination.resolve().parent!=root or destination.is_symlink():
            raise ValueError(f'Publication target must be a direct file in output: {name}')
    previous={}
    changed=[]
    try:
        for name,raw in operations:
            destination=output/name
            old=destination.read_bytes() if destination.exists() else None
            if old==raw: continue
            previous.setdefault(destination,old)
            if raw is None: destination.unlink()
            else: atomic_write(destination,raw)
            changed.append(name)
    except BaseException:
        for destination,old in previous.items():
            if old is None: destination.unlink(missing_ok=True)
            else: atomic_write(destination,old)
        raise
    return changed
