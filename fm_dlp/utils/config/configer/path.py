"""Persistent download path storage using JSON config file."""

from ...colors import (
    BOLD_GREEN,
    error,
    hint,
    info,
    set_colors,
    styled,
)
from . import CONFIG_FILE, Path, _load_config, _save_config, echo, sys

PATH_KEY = "path"


def set_path(path: str, color: bool) -> str:
    """Set and save the download directory path.

    Validates the path, creates parent directories if needed, and saves
    the configuration. Exits with error if path is invalid.

    Args:
        path: Directory path for downloads. Can be absolute or relative.
        color: Colored output in success/error messages.

    Returns:
        Success message with the configured path and config file location.

    Raises:
        SystemExit: If path is invalid or permission denied.
    """
    set_colors(color)
    try:
        input_path = str(Path(path).expanduser().resolve())

        if not Path(input_path).is_dir():
            echo(error("Please enter the correct path!"), file=sys.stderr)
            sys.exit(1)

        config = _load_config(color)
        config[PATH_KEY] = input_path

        if not _save_config(config):
            raise PermissionError()

        return styled("Configuration saved successfully", BOLD_GREEN)

    except PermissionError:
        return error(f"Permission denied! Cannot write to {CONFIG_FILE}")
    except OSError as e:
        return error(f"Error saving configuration: {e}")


def get_path(color: bool) -> str:
    """Get the configured download directory path.

    Returns the saved path from config or defaults to user's home directory
    if no configuration exists. Exits with error if saved path is invalid.

    Args:
        color: Colored output in error messages.

    Returns:
        String containing the download directory path.

    Raises:
        SystemExit: If saved path doesn't exist or is not a directory.
    """
    if not CONFIG_FILE.exists():
        echo(info("Home directory is used!"))
        echo(hint("Run the 'config' command to configure the download path\n"))
        return str(Path.home())

    data = _load_config(color)
    download_path = data.get(PATH_KEY)

    if not download_path or not Path(download_path).is_dir():
        set_colors(color)
        echo(error("Download path does not exist."), file=sys.stderr)
        sys.exit(1)

    return download_path
