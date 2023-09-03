import os
from typing import List

from ..system import SystemOS, run_command
from .consts import SystemNotSetupError


class Installer:
    def __init__(self, package_names=None):
        self.os = SystemOS.discover_os()
        if package_names is not None:
            self.install_system_packages(package_names)

    def install_system_packages(self, package_names: List[str], update_first=True):
        if self.os == SystemOS.LINUX:
            self.install_linux_packages(package_names, update_first=update_first)
        elif self.os == SystemOS.MAC:
            self.install_mac_packages(package_names, update_first=update_first)
        elif self.os == SystemOS.WINDOWS:
            raise NotImplementedError()
        else:
            raise Exception('Unknown OS')

    def install_linux_packages(self, package_names: List[str], update_first=True):
        installer = "apt"
        self.installer_is_installed(installer)

        if not self.user_is_root:
            installer = "sudo " + installer

        if update_first:
            run_command(f"{installer} update -y")

        packages = " ".join(package_names)
        stdout = run_command(f"{installer} install -y {packages}")
        if stdout is None:
            print(f"Failed to install packages: {packages}")

    def install_mac_packages(self, package_names: List[str], update_first=True):
        installer = "brew"
        self.installer_is_installed(installer)

        if update_first:
            run_command(f"{installer} update")

        breakpoint()
        packages = " ".join(package_names)
        stdout = run_command(f"{installer} install {packages}")
        if stdout is None:
            print(f"Failed to install packages: {packages}")

    #
    # Unix Utils
    #

    @property
    def user_is_root(self):
        return os.getuid() == 0

    def command_is_installed(self, package_name: str):
        if self.os not in [SystemOS.LINUX, SystemOS.MAC]:
            raise NotImplementedError()

        stdout = run_command(f"which {package_name}")
        if not stdout:
            return False

        return True

    def installer_is_installed(self, installer: str):
        if self.os not in [SystemOS.LINUX, SystemOS.MAC]:
            raise NotImplementedError()

        # sanity check installer
        if not self.command_is_installed(installer):
            raise SystemNotSetupError(f"Installer '{installer}' is not installed. Please install it.")

