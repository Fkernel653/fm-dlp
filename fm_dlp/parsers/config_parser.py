def create_config_parser(subparsers) -> None:
    """Create and configure the config command parser.

    Args:
        subparsers: Subparsers object from argparse.ArgumentParser.
    """

    config_parser = subparsers.add_parser(
        "config",
        help="Configure the application settings",
        description="Configure the application settings",
    )
    config_parser.add_argument(
        "path",
        help="Default directory path where downloaded files will be saved. Use absolute path for best results (e.g., '/home/user/Music' or 'C:\\Music').",
    )
