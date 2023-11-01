import platform
from pathlib import Path
import os
import signal
import shutil


#
# run system commands
#


class WorkDirContext:
    def __init__(self, path: Path):
        self.path = path
        self.origin = Path(os.getcwd()).absolute()

    def __enter__(self):
        os.chdir(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.origin)


def force_mkdir(path: Path):
    path = Path(path).expanduser().absolute()
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)

    try:
        os.mkdir(path)
    except Exception as e:
        print(f"Failed to make directory because {e}")


class unix_timeout:
    """
    A context manager for running a command with a timeout.
    Example use:
    try:
        with unix_timeout(seconds=5):
            run_command("sleep 10")
    except TimeoutError:
        print("Timed out!")
    """
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type_, value, traceback):
        signal.alarm(0)

