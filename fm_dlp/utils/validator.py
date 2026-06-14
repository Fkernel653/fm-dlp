"""Input validation module for fm-dlp CLI application."""

from functools import lru_cache
from pathlib import Path

from .colors import error, info, set_colors
from .functions import echo

AUDIO_CODECS = ("mp3", "aac", "flac", "m4a", "opus", "vorbis", "wav")
VIDEO_CONTAINERS = ("mp4", "mov", "mkv", "webm", "avi", "flv")
ALL_CODECS = AUDIO_CODECS + VIDEO_CONTAINERS


@lru_cache(maxsize=1)
def validate_ffmpeg(no_color: bool = False) -> bool:
    """Verify FFmpeg is installed.

    Args:
        no_color: Disable colored output in error messages.

    Returns:
        True if FFmpeg is found, False otherwise.
    """
    import shutil

    if no_color:
        set_colors(False)

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
    url: str | None = None,
    codec: str | None = None,
    kbps: int | None = None,
    jobs: int | None = None,
    path: str | None = None,
    no_color: bool = False,
) -> bool:
    """Validate all CLI download parameters.

    URL can be either a direct HTTP/HTTPS link or a path to a file with URLs.

    Args:
        url: URL to validate (HTTP/HTTPS or path to file).
        codec: Audio/video codec to validate.
        kbps: Bitrate to validate (64-320).
        jobs: Number of concurrent jobs to validate (>=1).
        path: Download directory path to validate.
        no_color: Disable colored output in validation messages.

    Returns:
        True if all parameters are valid, False otherwise.
    """
    if no_color:
        set_colors(False)

    # URL validation
    if url is not None:
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
                echo(
                    info(
                        "Must start with 'http://' or 'https://' or be a path to a file"
                    )
                )
                return False

    # Codec validation
    if codec is not None and codec not in ALL_CODECS:
        echo(error(f"Invalid codec: '{codec}'"))
        echo(info(f"Allowed values: {', '.join(ALL_CODECS)}"))
        return False

    # Bitrate validation
    if kbps is not None and (not isinstance(kbps, int) or not (64 <= kbps <= 320)):
        echo(error(f"Invalid bitrate: {kbps}"))
        echo(info("Must be an integer between 64 and 320."))
        return False

    # Jobs validation
    if jobs is not None and (not isinstance(jobs, int) or jobs < 1):
        echo(error(f"Invalid jobs: {jobs}"))
        echo(info("Must be an integer >= 1."))
        return False

    # Path validation
    if path is not None:
        real_path = Path(path)
        if real_path.is_file():
            echo(error("The path must not be a file"))
            echo(info("Enter the path to the folder"))
            return False
        elif not real_path.is_dir():
            if real_path.exists():
                echo(error(f"Path exists but is not a directory: '{path}'"))
                echo(info("Enter a valid directory path"))
                return False
            parent = real_path.parent
            if parent.exists() and not parent.is_dir():
                echo(error(f"Parent path is not a directory: '{parent}'"))
                return False
            return True
        return True

    return True
