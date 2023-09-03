import subprocess
import platform
from typing import Optional
from pathlib import Path
import os
import signal
import shutil
import re


#
# understand OS
#

class SystemOS:
    LINUX = 'linux'
    MAC = 'mac'
    WINDOWS = 'windows'
    UNKNOWN = 'unknown'

    @staticmethod
    def discover_os():
        if platform.system() == 'Linux':
            return SystemOS.LINUX
        elif platform.system() == 'Darwin':
            return SystemOS.MAC
        elif platform.system() == 'Windows':
            return SystemOS.WINDOWS
        else:
            return SystemOS.UNKNOWN

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


def user_is_root():
    if SystemOS.discover_os() not in [SystemOS.LINUX, SystemOS.MAC]:
        raise NotImplementedError()
    return os.getuid() == 0


def run_command(command: str, as_shell=False, normalize_cmd=True, is_root=None) -> Optional[str]:
    """
    Runs a command in the system. Returns either the stdout or None if it failed.

    :param command:
    :param as_shell:
    :param normalize_cmd:  Normalize the command before running it. This is useful for commands that use ~ or $.
    :return:
    """
    replaced_commands = list()
    if normalize_cmd:
        shell_strs = ["&&", "||", ">", "<", "|", ";", "&", "*", "$"]
        if any([s in command for s in shell_strs]):
            as_shell = True

        if "~" in command:
            # XXX: if a space is in this, it will break
            command = command.replace("~", str(Path.home()))

        is_root = is_root or user_is_root()
        if is_root and "sudo" in command:
            command = command.replace("sudo ", "")

    cmd_list = command.split(' ') if not as_shell else command
    try:
        out = subprocess.run(cmd_list, shell=as_shell, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        text = out.stdout.decode('utf-8').strip()
    except subprocess.CalledProcessError:
        text = None

    return text
