def create_config_parser(subparsers):
    config_parser = subparsers.add_parser(
        "config",
        help="Configure the application settings",
        description="Configure the application settings",
    )
    add_arg = config_parser.add_argument

    add_arg(
        "path",
        type=str,
        help="Default directory path where downloaded files will be saved. Use absolute path for best results (e.g., '/home/user/Music' or 'C:\\Music').",
    )
    add_arg(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress output messages.",
    )
    add_arg(
        "-C",
        "--config-file",
        type=str,
        metavar="PATH",
        help="Path to a custom TOML config file. Overrides the platform-specific default.",
    )
