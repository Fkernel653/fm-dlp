"""Persistent download path storage using JSON config file."""

import json
import os
import sys
from functools import lru_cache
from typing import Any

from ...utils import echo
from ..colors import (
    BOLD_GREEN,
    error,
    hint,
    info,
    set_colors,
    styled,
    success,
)
from ..config.path import Path


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
PATH_KEY = "path"
PARAM_KEY = "parameters"


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


def set_parameters(
    codec: str,
    kbps: int,
    quality: str | None,
    jobs: int,
    quiet: bool,
    metadata: bool,
    keep: bool,
    only_video: bool,
    cookies: str | None,
    color: bool,
) -> bool:
    """Save download parameters to config file without overwriting other settings.

    Args:
        codec: Audio codec or video container.
        kbps: Audio bitrate in kbps.
        quality: Video quality preset (best, 1080p, 720p, 480p, 360p, 2160p, worst).
        jobs: Maximum concurrent downloads.
        quiet: Suppress yt-dlp output.
        metadata: Embed metadata and thumbnail.
        keep: Keep the original downloaded file after conversion.
        only_video: Download video only.
        cookies: Path to cookies file or browser name.
        color: Colored output.

    Returns:
        True if parameters saved successfully, False otherwise.
    """
    set_colors(color)

    try:
        config = _load_config(color)

        config[PARAM_KEY] = {
            "codec": codec,
            "kbps": kbps,
            "quality": quality,
            "jobs": jobs,
            "quiet": quiet,
            "metadata": metadata,
            "keep": keep,
            "only_video": only_video,
            "cookies": cookies,
        }

        if not _save_config(config):
            raise PermissionError()

        if not quiet:
            echo(success("Parameters have been successfully saved"))
        return True

    except PermissionError:
        if not quiet:
            echo(
                error(f"Permission denied! Cannot write to {CONFIG_FILE}"),
                file=sys.stderr,
            )
        return False
    except OSError as e:
        if not quiet:
            echo(error(f"Error saving configuration: {e}"), file=sys.stderr)
        return False


def get_parameters(color: bool) -> dict[str, Any]:
    """Retrieve saved parameters from config file.

    Args:
        color: Colored output for error messages.

    Returns:
        Dictionary with saved parameters or empty dict if none exist.
    """
    set_colors(color)

    if not CONFIG_FILE.exists():
        return {}

    config = _load_config(color)
    return config.get(PARAM_KEY, {})
