"""Entry point for fm-dlp CLI."""

import sys

from color_kiss import GREEN, RED, RESET

from .cli import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{GREEN}Goodbye!{RESET}")
        sys.exit(0)
    except SystemExit as e:
        sys.exit(e.code if e.code is not None else 0)
    except Exception as e:
        sys.exit(f"{RED}\nUnexpected Error: {RESET}{e}")
