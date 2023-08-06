# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os
import tempfile

from .log import get_logger
from .. import APP_DEV

RUNTIME_DIRS = [
    "/var/run/es7s",
    "/tmp/es7s",
]
_runtime_dir: str | None = None


def get_socket_path(topic: str, write: bool):
    filename = f"{topic}.socket"
    path = os.path.join(_get_runtime_dir(write), filename)
    if APP_DEV:
        path += ".dev"
    return path


def get_daemon_lockfile_path():
    return os.path.join(_get_runtime_dir(), "es7s-daemon.lock")


def _get_runtime_dir(write: bool) -> str:
    global _runtime_dir
    if _runtime_dir:
        return _runtime_dir

    def try_read():
        open(os.path.join(runtime_dir, "es7s", "es7s-daemon.lock"), mode="rt").close()

    def try_write():
        os.makedirs(runtime_dir, exist_ok=True)
        tempfile.TemporaryFile(dir=runtime_dir).close()

    e = Exception("No runtime dirs provided")
    for runtime_dir in RUNTIME_DIRS:
        try:
            if not write:
                try_read()
            else:
                try_write()
            _runtime_dir = runtime_dir
        except Exception as e:
            get_logger(False).warning(
                f'Runtime dir is not {"writeable" if write else "readable"}: "{runtime_dir}"'
            )
            continue
        return runtime_dir
    raise OSError("Could not find suitable runtime directory") from e
