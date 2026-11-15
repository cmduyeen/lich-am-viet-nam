"""Standard-library-only, bounded atomic publication shared by CLI and CI."""

import os
import re
import tempfile
from pathlib import Path

_SAFE_NAME = re.compile(r"(?:[A-Za-z0-9][A-Za-z0-9_.-]*\.(?:ics|json|zip)|\.build-state\.json)")
_RESERVED = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}


def safe_filename(name):
    return (
        isinstance(name, str)
        and bool(_SAFE_NAME.fullmatch(name))
        and name.split(".")[0].upper() not in _RESERVED
    )


def atomic_write(path, raw):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == raw:
        return False
    temp = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as file:
            temp = Path(file.name)
            file.write(raw)
        os.replace(temp, path)
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)
    return True


def obsolete_exports(output, staging, manifest):
    """Prune only generated dated exports for active, non-custom feed prefixes.

    Latest URLs, unrelated files and custom snapshots are never selected here.
    Save optional historical snapshots outside output/ to retain them permanently.
    """
    output, staging = Path(output), Path(staging)
    if not output.exists():
        return []
    keep = {file.name for file in staging.iterdir()}
    prefixes = [
        entry["file"].removesuffix("_latest.ics")
        for entry in manifest
        if entry["file"].endswith("_latest.ics")
        and "_custom_" not in entry["file"]
        and not entry["file"].startswith("custom_")
    ]
    patterns = [
        re.compile(re.escape(prefix) + r"_(?:\d{4}(?:_\d{4})?\.ics|yearly_\d{4}_\d{4}\.zip)$")
        for prefix in prefixes
    ]
    result = []
    for file in output.iterdir():
        if file.is_file() and not file.is_symlink() and file.name not in keep:
            if any(pattern.fullmatch(file.name) for pattern in patterns):
                result.append(file.name)
    return sorted(result)


def publish_staged(staging, output, obsolete=()):
    """Publish validated files and retire managed exports; rollback on failure."""
    staging, output = Path(staging), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    root = output.resolve()
    files = sorted(staging.iterdir(), key=lambda p: p.name)
    for source in files:
        if not safe_filename(source.name) or source.is_symlink() or not source.is_file():
            raise ValueError(f"Invalid staged file: {source.name}")
    operations = [
        (source.name, source.read_bytes()) for source in files if source.name != "index.json"
    ]
    operations.extend((name, None) for name in obsolete)
    operations.extend(
        (source.name, source.read_bytes()) for source in files if source.name == "index.json"
    )
    for name, _ in operations:
        destination = output / name
        if (
            not safe_filename(name)
            or destination.resolve().parent != root
            or destination.is_symlink()
        ):
            raise ValueError(f"Publication target must be a direct file in output: {name}")
    previous = {}
    changed = []
    try:
        for name, raw in operations:
            destination = output / name
            old = destination.read_bytes() if destination.exists() else None
            if old == raw:
                continue
            previous.setdefault(destination, old)
            if raw is None:
                destination.unlink()
            else:
                atomic_write(destination, raw)
            changed.append(name)
    except BaseException:
        for destination, old in previous.items():
            if old is None:
                destination.unlink(missing_ok=True)
            else:
                atomic_write(destination, old)
        raise
    return changed
