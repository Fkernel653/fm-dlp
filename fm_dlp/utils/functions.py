import sys
from typing import TextIO


def echo(text: str, file: TextIO = sys.stdout) -> None:
    """Print message to file.

    Args:
        text: Message to print.
        file: File to write to (default: stdout).
    """
    file.write(text + "\n")


def get_version():
    """
    Extracts version from pyproject.toml
    """
    import tomllib

    from fm_dlp.utils.config.path import Path

    file = Path(__file__).parent.parent.parent / "pyproject.toml"

    data = tomllib.loads(file.read_text("utf-8"))
    return data.get("project", {}).get("version", "unknown")
