import argparse


def main():
    parser = argparse.ArgumentParser()

    #
    # system setup flags
    #

    parser.add_argument(
        "--setup-system", action="store_true", help="""
        Setup the current system like mahaloz would've wanted :). This will in install:
        system packages; python packages; CTF packages; configs (dotfiles).
        """
    )
    parser.add_argument(
        "--no-configs", action="store_true", default=False, help="""
        Don't install any configs.
        """
    )
    parser.add_argument(
        "--no-packages", action="store_true", default=False, help="""
        Don't install any packages.
        """
    )
    args = parser.parse_args()

    if args.setup_system:
        from .system_setup import setup_system
        setup_system(install_pkgs=not args.no_packages, install_configs=not args.no_configs)


if __name__ == "__main__":
    main()
