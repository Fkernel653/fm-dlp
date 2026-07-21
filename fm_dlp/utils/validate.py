"""Input validation module for fm-dlp CLI application."""

import sys
from functools import lru_cache

from ..utils import (
    ALL_CODECS,
    COOKIE_EXTENSIONS,
    SUPPORTED_BROWSERS,
    SUPPORTED_QUALITIES,
    echo,
)
from .colors import error, hint, set_colors
from .config.path import Path


def _fail(msg: str, tip: str | None = None) -> None:
    """Print error message and exit."""
    echo(error(msg), file=sys.stderr)
    if tip:
        echo(hint(tip))
    sys.exit(1)


def _check(condition: bool, msg: str, tip: str | None = None) -> None:
    """Check condition and exit with error if not met."""
    if not condition:
        _fail(msg, tip)


@lru_cache(maxsize=1)
def validate_ffmpeg(color: bool) -> None:
    """Verify FFmpeg is installed."""
    import shutil

    set_colors(color)

    _check(
        shutil.which("ffmpeg") is not None,
        "FFmpeg is not installed or not found in system PATH!",
        "Install FFmpeg and ensure it's accessible from the command line.",
    )


def _validate_url(url: str) -> None:
    """Validate URL or file path."""
    path = Path(url)

    if path.is_file():
        _check(path.stat().st_size > 0, f"URL file is empty: '{url}'")
        return

    _check(
        not path.exists(),
        f"Path exists but is not a file: '{url}'",
    )

    is_valid_url = url.startswith(("http://", "https://")) and url not in (
        "http://",
        "https://",
    )
    _check(
        is_valid_url,
        f"Invalid URL: '{url}'",
        "Must start with 'http://' or 'https://' and contain a valid address (not just the protocol)",
    )


def _validate_path(path: str) -> None:
    """Validate download directory path."""
    real_path = Path(path)

    _check(
        not real_path.is_file(),
        "The path must not be a file",
        "Enter the path to the folder",
    )

    _check(
        not (real_path.exists() and not real_path.is_dir()),
        f"Path exists but is not a directory: '{path}'",
        "Enter a valid directory path",
    )

    parent = real_path.parent
    _check(
        not (parent.exists() and not parent.is_dir()),
        f"Parent path is not a directory: '{parent}'",
    )


def _validate_cookies(cookies: str) -> None:
    """Validate cookies parameter (browser name or file path)."""
    _check(
        bool(cookies),
        "Cookies parameter cannot be empty",
        "Provide a browser name or path to cookie file",
    )

    cookies_path = Path(cookies)

    if cookies_path.exists():
        _check(
            cookies_path.is_file(),
            f"Path exists but is not a file: '{cookies}'",
            "Must be a path to a cookie file",
        )
        _check(
            cookies_path.stat().st_size > 0,
            f"Cookie file is empty: '{cookies}'",
        )
        _check(
            cookies_path.suffix.lower() in COOKIE_EXTENSIONS,
            f"Cookie file has unusual extension: '{cookies_path.suffix}'",
            "Expected .txt (Netscape format), .sqlite, .db, or .cookies",
        )
    else:
        _check(
            cookies.lower() in SUPPORTED_BROWSERS,
            f"Unsupported browser: '{cookies}'",
            f"Supported browsers: {', '.join(sorted(SUPPORTED_BROWSERS))}. Or provide a path to a cookie file",
        )


def _validate_quality(quality: str) -> None:
    """Validate video quality parameter."""
    quality_lower = quality.lower().strip()

    if quality_lower in SUPPORTED_QUALITIES:
        return

    if quality_lower.isdigit():
        height = int(quality_lower)
        _check(
            height > 0,
            f"Invalid height: {height}",
            "Height must be a positive integer (e.g., 720, 1080, 2160)",
        )
        return

    if quality_lower.endswith("p") and quality_lower[:-1].isdigit():
        height = int(quality_lower[:-1])
        _check(
            height > 0,
            f"Invalid height: {height}",
            "Height must be a positive integer (e.g., 720p, 1080p, 2160p)",
        )
        return

    _fail(
        f"Warning: Unusual quality format '{quality}'. yt-dlp will attempt to handle it.",
        "Recommended formats: best, worst, 1080p, 720p, 480p, or custom height like 720",
    )


def validate_download(
    url: str,
    codec: str,
    kbps: int,
    quality: str,
    jobs: int,
    path: str,
    cookies: str | None,
    color: bool,
) -> None:
    """Validate all CLI download parameters."""
    set_colors(color)

    _validate_url(url)
    _check(
        codec in ALL_CODECS,
        f"Invalid codec: '{codec}'",
        f"Allowed values: {', '.join(ALL_CODECS)}",
    )
    _check(
        64 <= kbps <= 320,
        f"Invalid bitrate: {kbps}",
        "Must be an integer between 64 and 320",
    )
    _validate_quality(quality)
    _check(
        jobs >= 1,
        f"Invalid jobs: {jobs}",
        "Must be an integer >= 1",
    )
    _validate_path(path)
    if cookies is not None:
        _validate_cookies(cookies)


def validate_search(limit: int, color: bool) -> None:
    """Validate search limit parameter."""
    set_colors(color)
    _check(
        limit > 0,
        f"Invalid limit: {limit}",
        "Must be a positive integer",
    )
