"""Input validation module for fm-dlp CLI application."""

from functools import lru_cache
from pathlib import Path
from typing import Any

from .colors import error, info, set_colors
from .functions import echo

AUDIO_CODECS = {"mp3", "aac", "flac", "m4a", "opus", "vorbis", "wav"}
VIDEO_CONTAINERS = {"mp4", "mov", "mkv", "webm", "avi", "flv"}
ALL_CODECS = AUDIO_CODECS | VIDEO_CONTAINERS
SUPPORTED_BROWSERS = {
    "brave",
    "chrome",
    "chromium",
    "edge",
    "firefox",
    "opera",
    "safari",
    "vivaldi",
    "whale",
}


@lru_cache(maxsize=1)
def validate_ffmpeg(color: bool) -> bool:
    """Verify FFmpeg is installed.

    Args:
        color: Colored output in error messages.

    Returns:
        True if FFmpeg is found, False otherwise.
    """
    import shutil

    set_colors(color)

    target = "ffmpeg"
    name = "FFmpeg"
    if shutil.which(target) is None:
        echo(error(f"{name} is not installed or not found in system PATH!"))
        echo(
            info(
                f"Please install {name} and ensure it's accessible from the command line."
            )
        )
        echo(info(f"Tip: Run '{target} --version' to verify installation."))
        return False
    return True


def validate_download(
    url: str,
    codec: str,
    kbps: int,
    jobs: int,
    path: str,
    color: bool,
    cookies: str | None = None,
) -> bool:
    """Validate all CLI download parameters.

    URL can be either a direct HTTP/HTTPS link or a path to a file with URLs.

    Args:
        url: URL to validate (HTTP/HTTPS or path to file).
        codec: Audio/video codec to validate.
        kbps: Bitrate to validate (64-320).
        jobs: Number of concurrent jobs to validate (>=1).
        path: Download directory path to validate.
        color: Colored output in validation messages.
        cookies: Browser name for cookie extraction or path to cookie file (optional).

    Returns:
        bool: True if all parameters are valid, False otherwise.
    """
    set_colors(color)

    # URL validation
    if not isinstance(url, str) or not url.strip():
        echo(error("URL cannot be empty or whitespace only"))
        return False

    url_path = Path(url)

    if url_path.is_file():
        if url_path.stat().st_size == 0:
            echo(error(f"URL file is empty: '{url}'"))
            return False
    elif url_path.exists():
        echo(error(f"Path exists but is not a file: '{url}'"))
        return False
    else:
        if not (url.startswith("http://") or url.startswith("https://")):
            echo(error(f"Invalid URL: '{url}'"))
            echo(info("Must start with 'http://' or 'https://' or be a path to a file"))
            return False

    # Codec validation
    if codec not in ALL_CODECS:
        echo(error(f"Invalid codec: '{codec}'"))
        echo(info(f"Allowed values: {', '.join(ALL_CODECS)}"))
        return False

    # Bitrate validation
    if kbps < 64 or kbps > 320:
        echo(error(f"Invalid bitrate: {kbps}"))
        echo(info("Must be an integer between 64 and 320."))
        return False

    # Jobs validation
    if jobs < 1:
        echo(error(f"Invalid jobs: {jobs}"))
        echo(info("Must be an integer >= 1."))
        return False

    # Path validation
    real_path = Path(path)

    if real_path.is_file():
        echo(error("The path must not be a file"))
        echo(info("Enter the path to the folder"))
        return False

    if real_path.exists() and not real_path.is_dir():
        echo(error(f"Path exists but is not a directory: '{path}'"))
        echo(info("Enter a valid directory path"))
        return False

    parent = real_path.parent
    if parent.exists() and not parent.is_dir():
        echo(error(f"Parent path is not a directory: '{parent}'"))
        return False

    # Cookies validation (optional)
    if cookies is not None:
        cookies = cookies.strip()
        if not cookies:
            echo(error("Cookies parameter cannot be empty"))
            echo(info("Provide a browser name or path to cookie file"))
            return False

        cookies_path = Path(cookies)
        if cookies_path.exists():
            if cookies_path.is_file():
                if cookies_path.stat().st_size == 0:
                    echo(error(f"Cookie file is empty: '{cookies}'"))
                    return False
                if cookies_path.suffix.lower() not in {
                    ".txt",
                    ".sqlite",
                    ".db",
                    ".cookies",
                }:
                    echo(
                        error(
                            f"Cookie file has unusual extension: '{cookies_path.suffix}'",
                        )
                    )
                    echo(
                        info(
                            "Expected .txt (Netscape format), .sqlite, .db, or .cookies"
                        )
                    )
                    return False
            else:
                echo(error(f"Path exists but is not a file: '{cookies}'"))
                echo(info("Must be a path to a cookie file"))
                return False
        else:
            browser_name = cookies.lower()
            if browser_name not in SUPPORTED_BROWSERS:
                echo(error(f"Unsupported browser: '{cookies}'"))
                echo(
                    info(f"Supported browsers: {', '.join(sorted(SUPPORTED_BROWSERS))}")
                )
                echo(info("Or provide a path to a cookie file"))
                return False

    return True


def validate_search(limit: Any, color: bool) -> bool:
    """
    Validate the search limit parameter.

    This function validates that the provided limit is a positive integer.
    If the limit is None, it defaults to 10. If the limit is invalid
    (non-integer or non-positive), an error message is displayed and
    False is returned.

    Args:
        limit (Any): The limit value to validate. Can be any type,
                     but should be convertible to an integer.
        color (bool): Flag indicating whether to use colored output
                      for error and info messages.

    Returns:
        bool: True if the limit is valid (positive integer or None),
              False otherwise.
    """
    set_colors(color)
    try:
        limit_int = int(limit) if limit is not None else 10
        if limit_int <= 0:
            echo(error(f"Invalid limit: {limit}"))
            echo(info("Must be a positive integer."))
            return False
        return True
    except (TypeError, ValueError):
        echo(error(f"Invalid limit: {limit}"))
        echo(info("Must be an integer."))
        return False
