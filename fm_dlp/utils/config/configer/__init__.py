import json
import os
import sys
from functools import lru_cache

from ....utils import echo
from ...colors import error, set_colors
from ..path import Path


def _get_config_dir() -> str:
    """Get the user config directory based on platform."""
    home = Path.home()

    if sys.platform == "win32":
        appdata = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
        d = Path(appdata) if appdata else (home / "AppData" / "Local")
    elif sys.platform == "darwin":
        d = home / "Library" / "Application Support"
    else:
        xdg = os.environ.get("XDG_CONFIG_HOME")
        d = Path(xdg) if xdg else (home / ".config")

    return str(d / "fm-dlp")


CONFIG_DIR = _get_config_dir()
CONFIG_FILE = Path(CONFIG_DIR) / "config.json"


@lru_cache(maxsize=1)
def _load_config(color: bool) -> dict:
    """Load configuration from JSON file with caching.

    Args:
        color: Colored output for error messages.

    Returns:
        Dictionary containing configuration data. Empty dict if file doesn't exist.
    """
    if not CONFIG_FILE.exists():
        return {}
    try:
        return json.loads(CONFIG_FILE.read_text("utf-8"))
    except (json.JSONDecodeError, OSError):
        set_colors(color)
        echo(error("Config file is corrupted. Creating new one..."), file=sys.stderr)
        return {}


def _save_config(data: dict) -> bool:
    """Save configuration data to JSON file."""
    try:
        CONFIG_FILE.parent.mkdir(exist_ok=True)
        CONFIG_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=4), "utf-8")
        _load_config.cache_clear()
        return True
    except (PermissionError, OSError):
        return False
