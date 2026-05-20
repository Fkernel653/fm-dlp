"""
Persistent download path storage using JSON config file.
Cross-platform config management via platformdirs.
"""

import json
import sys
from pathlib import Path

from color_kiss import BLUE, GRAY, RESET
from color_kiss.utils import error, styled, success
from platformdirs import user_config_dir

# Cross-platform paths:
# Windows: %APPDATA%/fm-dlp/
# macOS:   ~/Library/Application Support/fm-dlp/
# Linux:   ~/.config/fm-dlp/
CONFIG_DIR = Path(user_config_dir("fm-dlp"))
CONFIG_FILE = CONFIG_DIR / "config.json"
HOME_PATH: str = str(Path.home())

KEY_NAME: str = "path"


def _ensure_config_dir() -> None:
    """Create config directory if it doesn't exist."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def _load_config() -> dict:
    """Load config file or return empty dict if not exists."""
    if not CONFIG_FILE.exists():
        return {}

    try:
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        error("Config file is corrupted. Creating new one...")
        return {}


def _save_config(data: dict) -> None:
    """Save config data to file."""
    _ensure_config_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def set_path(path: str) -> str:
    """
    Manage download directory storage.
    - With path: saves to config.json
    - Without path: displays current config
    """
    try:
        input_path = Path(path).expanduser().resolve()
        if not input_path.is_dir():
            sys.exit(error("Please enter the correct path!"))

        path_str = str(input_path)

        _ensure_config_dir()
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({KEY_NAME: path_str}, f, ensure_ascii=False, indent=4)

        return success(f"\nPath: {path_str}\nConfig file: {CONFIG_FILE}")
    except PermissionError:
        return error(f"\nPermission denied! Cannot write to {CONFIG_FILE}")
    except OSError as e:
        return error(f"\nError saving configuration: {e}")


def get_path() -> str:
    """
    Get configured download path or prompt user to set one.

    Returns:
        str: Valid download path or None if not configured
    """
    if not CONFIG_FILE.exists():
        error("\nConfig file not found!\n")
        styled("Run: fm-dlp config /path or continue in the home directory\n", GRAY)
        user_input = input(
            f"{BLUE}Do you want to continue in the home directory? (Y/n): {RESET}"
        )
        if user_input.lower() == "y":
            return HOME_PATH
        else:
            sys.exit(1)

    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        sys.exit(error("\nConfig file is corrupted."))

    download_path = data.get(KEY_NAME)

    if not download_path or not Path(download_path).is_dir():
        sys.exit(error("\nDownload path does not exist."))

    return download_path
