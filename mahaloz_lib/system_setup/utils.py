import subprocess
from typing import Optional


def run_command(command: str, as_shell=False) -> Optional[str]:
    """
    Runs a command in the system. Returns either the stdout or None if it failed.

    :param command:
    :param as_shell:
    :return:
    """
    cmd_list = command.split(' ')
    try:
        out = subprocess.run(cmd_list, shell=as_shell, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        text = out.stdout.decode('utf-8').strip()
    except subprocess.CalledProcessError:
        text = None

    return text
