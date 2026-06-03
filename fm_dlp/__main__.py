"""Entry point for fm-dlp CLI."""

import sys

from color_kiss import GREEN, RED
from color_kiss.utils import styled

from .utils.functions import echo

if __name__ == "__main__":
    try:
        from .cli import main

        main()
    except KeyboardInterrupt:
        echo(styled("\nGoodbye!\n", GREEN))
        sys.exit(0)
    except SystemExit as e:
        sys.exit(e.code if e.code is not None else 0)
    except Exception as e:
        echo(styled(f"\nUnexpected Error: {e}\n", RED), file=sys.stderr)
        sys.exit(1)
