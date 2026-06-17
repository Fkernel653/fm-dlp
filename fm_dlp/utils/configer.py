"""Persistent download path storage using JSON config file."""

import json
import sys
from functools import lru_cache
from pathlib import Path

from platformdirs import user_config_dir

from .colors import error, set_colors, success
from .functions import echo

CONFIG_DIR = Path(user_config_dir("fm-dlp"))
CONFIG_FILE = CONFIG_DIR / "config.json"
HOME_PATH = str(Path.home())
KEY_NAME = "path"


@lru_cache(maxsize=1)
def _load_config(color: bool) -> dict:
    """Load configuration from JSON file with caching.

    Args:
        no_color: Disable colored output for error messages.

    Returns:
        Dictionary containing configuration data. Empty dict if file doesn't exist.
    """
    if not CONFIG_FILE.exists():
        return {}
    try:
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        set_colors(color)
        echo(error("Config file is corrupted. Creating new one..."))
        return {}


def _save_config(data: dict) -> None:
    """Save configuration data to JSON file.

    Creates the config directory if it doesn't exist.

    Args:
        data: Dictionary containing configuration data to save.
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )


def set_path(path: str, color: bool) -> str:
    """Set and save the download directory path.

    Validates the path, creates parent directories if needed, and saves
    the configuration. Exits with error if path is invalid.

    Args:
        path: Directory path for downloads. Can be absolute or relative.
        no_color: Disable colored output in success/error messages.

    Returns:
        Success message with the configured path and config file location.

    Raises:
        SystemExit: If path is invalid or permission denied.
    """
    set_colors(color)
    try:
        input_path = Path(path).expanduser().resolve()
        if not input_path.is_dir():
            echo(error("Please enter the correct path!"), file=sys.stderr)
            sys.exit(1)

        _save_config({KEY_NAME: str(input_path)})
        _load_config.cache_clear()
        return success(f"\nPath: {input_path}\nConfig file: {CONFIG_FILE}")
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
        return HOME_PATH
    data = _load_config(color)
    download_path = data.get(KEY_NAME)

    if not download_path or not Path(download_path).is_dir():
        set_colors(color)
        echo(error("Download path does not exist."), file=sys.stderr)
        sys.exit(1)

    return download_path
