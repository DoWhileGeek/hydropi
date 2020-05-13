import os
import sys
from contextlib import contextmanager
import tempfile
import logging


@contextmanager
def pid_lock():
    perform_finally = True

    try:
        pid = str(os.getpid())
        pidfile = os.path.join(tempfile.gettempdir(), "hydropi.pid")

        if os.path.isfile(pidfile):
            logging.debug("script already running, exiting")
            perform_finally = False
            sys.exit()

        with open(pidfile, "w") as f:
            f.write(pid)

        yield pid
    finally:
        if perform_finally:
            print("bang")
            os.remove(pidfile)
