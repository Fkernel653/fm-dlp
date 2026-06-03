"""Persistent download path storage using JSON config file."""

import json
import sys
from functools import lru_cache
from pathlib import Path

from color_kiss.utils import error, info, success
from platformdirs import user_config_dir

CONFIG_DIR = Path(user_config_dir("fm-dlp"))
CONFIG_FILE = CONFIG_DIR / "config.json"
HOME_PATH = str(Path.home())
KEY_NAME = "path"


def _ensure_config_dir() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def _load_config() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    try:
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        error("Config file is corrupted. Creating new one...")
        return {}


def _save_config(data: dict) -> None:
    _ensure_config_dir()
    CONFIG_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )


def set_path(path: str) -> str:
    try:
        from functions import echo

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


def get_path() -> str:
    from functions import echo

    if not CONFIG_FILE.exists():
        echo(info("Config file not found! Home directory is used"), file=sys.stderr)
        return HOME_PATH
    data = _load_config()
    download_path = data.get(KEY_NAME)

    if not download_path or not Path(download_path).is_dir():
        echo(error("Download path does not exist."), file=sys.stderr)
        sys.exit(1)

    return download_path
