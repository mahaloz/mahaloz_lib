from pathlib import Path
import os
import logging

import toml

from .installer import Installer
from ..system import run_command, WorkDirContext


_l = logging.getLogger(__name__)
FILE_LOCATION = Path(os.path.dirname(os.path.realpath(__file__))).absolute()

#
# system setup
#


def _load_configs():
    configs_dir = FILE_LOCATION / "data" / "configs"
    configs = {}
    for setup_path in configs_dir.rglob("setup.toml"):
        with open(setup_path) as fp:
            configs[setup_path.parent.name] = toml.load(fp)

    return configs


def _load_packages():
    with open(FILE_LOCATION / "data" / "packages.toml") as fp:
        return toml.load(fp)


def setup_system(install_pkgs=True,  install_configs=True):

    #
    # install system packages
    #

    inst = Installer()
    if install_pkgs:
        packages = _load_packages()
        default_packages = packages["defaults"]

        # packages for all system OSes
        any_packages = default_packages["any"]
        _l.info(f"Installing {len(any_packages)} ANY system packages...")
        inst.install_system_packages(any_packages)

        # packages for specific system OSes
        os_packages = default_packages.get(inst.os, None)
        _l.info(f"Installing {len(os_packages)} {inst.os} system packages...")
        inst.install_system_packages(os_packages)

        _l.info("Installation complete!")

    #
    # config setup
    #

    if install_configs:
        configs = _load_configs()
        for config_name, config in configs.items():
            platforms = config["platforms"]
            if inst.os not in platforms:
                continue

            enabled = config.get("enabled", True)
            if not enabled:
                continue

            _l.info(f"Setting up {config_name}...")
            for cmd in config["commands"]:
                with WorkDirContext(FILE_LOCATION / "data" / "configs" / config_name):
                    output = run_command(cmd, is_root=inst.user_is_root)
                    if output is None:
                        _l.warning(f"Failed to install {config_name} on command {cmd}. Skipping...")
                        break

        _l.info("Config setup complete!")
