import sys
from typing import TextIO


def echo(text: str, file: TextIO = sys.stdout) -> None:
    """Print message to file.

    Args:
        text: Message to print.
        file: File to write to (default: stdout).
    """
    file.write(text + "\n")
