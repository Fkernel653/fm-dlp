"""
Persistent download path storage using JSON config file.
Cross-platform config management via platformdirs.
"""

import json
import sys
from pathlib import Path
from typing import Optional

from color_kiss import BLUE, GRAY, GREEN, RED, RESET, YELLOW
from platformdirs import user_config_dir

# Cross-platform paths:
# Windows: %APPDATA%/fm-dlp/
# macOS:   ~/Library/Application Support/fm-dlp/
# Linux:   ~/.config/fm-dlp/
CONFIG_DIR = Path(user_config_dir("fm-dlp"))
CONFIG_FILE = CONFIG_DIR / "config.json"
HOME_PATH = str(Path.home())

KEY_NAME = "path"


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
        print(f"{RED}Config file is corrupted. Creating new one...{RESET}")
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
            return f"{RED}Please enter the correct path!{RESET}"

        path_str = str(input_path)

        _ensure_config_dir()
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({KEY_NAME: path_str}, f, ensure_ascii=False, indent=4)

        return (
            f"{GREEN}\nConfiguration saved successfully!{RESET}\n"
            f"{YELLOW}Path: {RESET}{path_str}\n"
            f"{BLUE}Config file: {RESET}{CONFIG_FILE}"
        )
    except PermissionError:
        return f"{RED}\nPermission denied! Cannot write to {CONFIG_FILE}{RESET}"
    except OSError as e:
        return f"{RED}\nError saving configuration: {e}{RESET}"


def get_path() -> Optional[str]:
    """
    Get configured download path or prompt user to set one.

    Returns:
        str: Valid download path or None if not configured
    """
    if not CONFIG_FILE.exists():
        print(
            f"{RED}\nConfig file not found!{RESET}\n"
            f"{GRAY}Run: fm-dlp config /path or continue in the home directory{RESET}\n"
        )
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
        print(f"{RED}Config file is corrupted.{RESET}")
        sys.exit(1)

    download_path = data.get(KEY_NAME)

    if not download_path or not Path(download_path).is_dir():
        print(f"{RED}\nDownload path does not exist.{RESET}")
        sys.exit(1)

    return download_path
