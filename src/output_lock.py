"""Cross-platform process lock, released by the OS even after a crash."""
from contextlib import contextmanager
from pathlib import Path
import os

@contextmanager
def output_lock(output):
    output=Path(output).resolve()
    output.parent.mkdir(parents=True,exist_ok=True)
    path=output.parent/f'.lunar-{output.name}.lock'
    if path.is_symlink():raise ValueError('Output lock must not be a symbolic link')
    with path.open('a+b') as file:
        if os.fstat(file.fileno()).st_size==0:
            file.write(b'0');file.flush()
        file.seek(0)
        if os.name=='nt':
            import msvcrt
            try:msvcrt.locking(file.fileno(),msvcrt.LK_NBLCK,1)
            except OSError as exc:raise ValueError('Another generator is writing this output; retry after it finishes') from exc
        else:
            import fcntl
            try:fcntl.flock(file,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except OSError as exc:raise ValueError('Another generator is writing this output; retry after it finishes') from exc
        try:yield
        finally:
            file.seek(0)
            if os.name=='nt':msvcrt.locking(file.fileno(),msvcrt.LK_UNLCK,1)
            else:fcntl.flock(file,fcntl.LOCK_UN)
