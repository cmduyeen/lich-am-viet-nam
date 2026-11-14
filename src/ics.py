"""Wire validation, stable revisions and atomic file replacement."""

import zipfile
from copy import deepcopy
from datetime import date, datetime, timezone
from pathlib import Path

from icalendar import Calendar, Event

from .files import atomic_write, obsolete_exports, publish_staged

__all__ = [
    "atomic_write",
    "obsolete_exports",
    "publish_staged",
    "write_calendar",
    "validate_bytes",
    "reconcile",
    "create_zip",
]

_REVISION_FIELDS = {"DTSTAMP", "LAST-MODIFIED", "SEQUENCE", "CREATED"}


def _fingerprint(event):
    value = Event()
    for key, prop in event.items():
        if key not in _REVISION_FIELDS:
            value[key] = prop
    return value.to_ical()


def reconcile(calendar, previous=None):
    """Keep unmodified events byte-stable; update changed events under the same UID."""
    result = deepcopy(calendar)
    prior = {}
    if previous and Path(previous).exists():
        old = Calendar.from_ical(Path(previous).read_bytes())
        prior = {str(e["uid"]): e for e in old.walk("VEVENT")}
    now = datetime.now(timezone.utc).replace(microsecond=0)
    for event in result.walk("VEVENT"):
        old = prior.get(str(event["uid"]))
        if old is None:
            continue
        try:
            old_stamp = old.decoded("dtstamp")
            valid_stamp = (
                isinstance(old_stamp, datetime)
                and old_stamp.tzinfo is not None
                and old_stamp.utcoffset().total_seconds() == 0
            )
        except (ValueError, KeyError):
            valid_stamp = False
        if valid_stamp and _fingerprint(old) == _fingerprint(event):
            for key in _REVISION_FIELDS:
                event.pop(key, None)
                if key in old:
                    event[key] = old[key]
        else:
            event.pop("DTSTAMP", None)
            event.pop("LAST-MODIFIED", None)
            event.add("DTSTAMP", now)
            event.add("LAST-MODIFIED", now)
            event["SEQUENCE"] = int(old.get("SEQUENCE", 0)) + 1
    return result


def validate_bytes(raw):
    if b"\n" in raw.replace(b"\r\n", b""):
        raise ValueError("ICS must use CRLF line endings")
    if any(len(line) > 75 for line in raw.split(b"\r\n")):
        raise ValueError("ICS lines must be folded within 75 bytes")
    calendar = Calendar.from_ical(raw)
    seen = set()
    for event in calendar.walk("VEVENT"):
        uid = str(event["uid"])
        if uid in seen:
            raise ValueError(f"Duplicate UID: {uid}")
        seen.add(uid)
        first, last = event.decoded("dtstart"), event.decoded("dtend")
        if type(first) is not date or type(last) is not date or (last - first).days != 1:
            raise ValueError("Events must have one-day DATE boundaries")
        if not str(event["summary"]):
            raise ValueError("Empty event summary")
        stamp = event.decoded("dtstamp")
        if (
            not isinstance(stamp, datetime)
            or stamp.tzinfo is None
            or stamp.utcoffset().total_seconds() != 0
        ):
            raise ValueError("DTSTAMP must be a valid UTC datetime")
    return calendar


def write_calendar(calendar, path, previous=None, *, reconciled=False):
    value = calendar if reconciled else reconcile(calendar, previous or path)
    raw = value.to_ical()
    validate_bytes(raw)
    atomic_write(path, raw)
    return value


def create_zip(files, target):
    """Fixed ZIP metadata avoids a different archive on each generation."""
    target = Path(target)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(map(Path, files)):
            info = zipfile.ZipInfo(path.name, (2000, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
    with zipfile.ZipFile(target) as archive:
        if archive.testzip() is not None:
            raise ValueError("Corrupt ZIP archive")
