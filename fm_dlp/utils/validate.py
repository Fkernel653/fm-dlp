"""Input validation module for fm-dlp CLI application."""

from functools import lru_cache
from pathlib import Path

from fm_dlp.utils.colors import error, info, set_colors
from fm_dlp.utils.functions import echo

AUDIO_CODECS = {"mp3", "aac", "flac", "m4a", "opus", "vorbis", "wav", "alac"}
VIDEO_CONTAINERS = {"mp4", "mov", "mkv", "webm", "avi", "flv"}
ALL_CODECS = AUDIO_CODECS | VIDEO_CONTAINERS
SUPPORTED_BROWSERS = {
    "brave",
    "chrome",
    "chromium",
    "edge",
    "opera",
    "vivaldi",
    "whale",
    "firefox",
    "safari",
}
COOKIE_EXTENSIONS = {".txt", ".sqlite", ".db", ".cookies"}


def _fail(msg: str, hint: str | None = None) -> bool:
    """Print error message and return False."""
    echo(error(msg))
    if hint:
        echo(info(hint))
    return False


def _check(condition: bool, msg: str, hint: str | None = None) -> bool:
    """Check condition and return False with error if not met."""
    return condition or _fail(msg, hint)


@lru_cache(maxsize=1)
def validate_ffmpeg(color: bool) -> bool:
    """Verify FFmpeg is installed."""
    import shutil

    set_colors(color)

    return _check(
        shutil.which("ffmpeg") is not None,
        "FFmpeg is not installed or not found in system PATH!",
        "Install FFmpeg and ensure it's accessible from the command line.\nTip: Run 'ffmpeg --version' to verify installation.",
    )


def _validate_url(url: str) -> bool:
    """Validate URL or file path."""
    path = Path(url)

    if path.is_file():
        return _check(path.stat().st_size > 0, f"URL file is empty: '{url}'")
    if path.exists():
        return _fail(f"Path exists but is not a file: '{url}'")
    return _check(
        url.startswith(("http://", "https://")),
        f"Invalid URL: '{url}'",
        "Must start with 'http://' or 'https://' or be a path to a file",
    )


def _validate_path(path: str) -> bool:
    """Validate download directory path."""
    real_path = Path(path)

    if real_path.is_file():
        return _fail("The path must not be a file", "Enter the path to the folder")
    if real_path.exists() and not real_path.is_dir():
        return _fail(
            f"Path exists but is not a directory: '{path}'",
            "Enter a valid directory path",
        )

    parent = real_path.parent
    if parent.exists() and not parent.is_dir():
        return _fail(f"Parent path is not a directory: '{parent}'")

    return True


def _validate_cookies(cookies: str) -> bool:
    """Validate cookies parameter (browser name or file path)."""
    if not cookies:
        return _fail(
            "Cookies parameter cannot be empty",
            "Provide a browser name or path to cookie file",
        )

    cookies_path = Path(cookies)

    if cookies_path.exists():
        if not cookies_path.is_file():
            return _fail(
                f"Path exists but is not a file: '{cookies}'",
                "Must be a path to a cookie file",
            )
        if cookies_path.stat().st_size == 0:
            return _fail(f"Cookie file is empty: '{cookies}'")
        if cookies_path.suffix.lower() not in COOKIE_EXTENSIONS:
            return _fail(
                f"Cookie file has unusual extension: '{cookies_path.suffix}'",
                "Expected .txt (Netscape format), .sqlite, .db, or .cookies",
            )
    else:
        if cookies.lower() not in SUPPORTED_BROWSERS:
            return _fail(
                f"Unsupported browser: '{cookies}'",
                f"Supported browsers: {', '.join(sorted(SUPPORTED_BROWSERS))}\nOr provide a path to a cookie file",
            )

    return True


def validate_download(
    url: str,
    codec: str,
    kbps: int,
    jobs: int,
    path: str,
    cookies: str | None,
    color: bool,
) -> bool:
    """Validate all CLI download parameters."""
    set_colors(color)

    return (
        _validate_url(url)
        and _check(
            codec in ALL_CODECS,
            f"Invalid codec: '{codec}'",
            f"Allowed values: {', '.join(ALL_CODECS)}",
        )
        and _check(
            64 <= kbps <= 320,
            f"Invalid bitrate: {kbps}",
            "Must be an integer between 64 and 320",
        )
        and _check(jobs >= 1, f"Invalid jobs: {jobs}", "Must be an integer >= 1")
        and _validate_path(path)
        and (cookies is None or _validate_cookies(cookies))
    )


def validate_search(limit: int, color: bool) -> bool:
    """Validate search limit parameter."""
    set_colors(color)
    return _check(limit > 0, f"Invalid limit: {limit}", "Must be a positive integer")
