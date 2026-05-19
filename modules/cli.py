"""
CLI entry point for fm-dlp using argparse library.
Commands: search, download, config
"""

import sys

from color_kiss import GREEN, RED, RESET


def get_version() -> str:
    """Get version from installed package metadata."""
    try:
        from importlib.metadata import version

        return version("fm-dlp")
    except Exception:
        return "unknown"


def main() -> None:
    """Main entry point for the CLI."""
    from modules.parser import create_parser

    parser = create_parser(get_version())
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    match args.command:
        case "search":
            from modules.handlers import handle_search

            handle_search(args)
        case "download":
            from modules.handlers import handle_download

            handle_download(args)
        case "config":
            from modules.handlers import handle_config

            handle_config(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{GREEN}Goodbye!{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{RED}Unexpected Error:{RESET} {e}")
        sys.exit(1)
