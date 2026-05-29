"""Input validation module for fm-dlp CLI application."""

import sys
from typing import Any, Literal, TypeAlias

AUDIO_CODECS = ("mp3", "aac", "flac", "m4a", "opus", "vorbis", "wav")
VIDEO_CONTAINERS = ("mp4", "mov", "mkv", "webm", "avi", "flv")
ALL_CODECS = AUDIO_CODECS + VIDEO_CONTAINERS
DEFAULT_CODEC = "m4a" if sys.platform == "darwin" else "opus"

Codec: TypeAlias = Literal[
    "mp3",
    "aac",
    "flac",
    "m4a",
    "opus",
    "vorbis",
    "wav",
    "mp4",
    "mov",
    "mkv",
    "webm",
    "avi",
    "flv",
]
SearchType: TypeAlias = Literal["track", "album"]


class ValidationError(ValueError):
    """Base validation error."""


def validate_with_shutil(target: str, text: str) -> None:
    """Verify a system dependency is installed."""
    import shutil

    if shutil.which(target) is None:
        raise ValidationError(
            f"{text} is not installed or not found in system PATH!\n"
            f"Please install {text} and ensure it's accessible from the command line.\n"
            f"Tip: Run '{target} --version' to verify installation."
        )


def validate_input(**kwargs: Any) -> None:
    """Validate all CLI input parameters.

    Args:
        **kwargs: Input parameters to validate.

    Raises:
        ValidationError: If any parameter fails validation.
    """

    # Codec
    codec = kwargs.get("codec")
    if codec is not None:
        if codec not in ALL_CODECS:
            raise ValidationError(
                f"Invalid codec: '{codec}'. Allowed values: {', '.join(ALL_CODECS)}"
            )

    # Bitrate
    kbps = kwargs.get("kbps")
    if kbps is not None:
        if not isinstance(kbps, int) or not (64 <= kbps <= 320):
            raise ValidationError(
                f"Invalid bitrate: {kbps}. Must be an integer between 64 and 320."
            )

    # Jobs
    jobs = kwargs.get("jobs")
    if jobs is not None:
        if not isinstance(jobs, int) or jobs < 1:
            raise ValidationError(f"Invalid jobs: {jobs}. Must be an integer >= 1.")

    # Limit
    limit = kwargs.get("limit")
    if limit is not None:
        if not isinstance(limit, int) or limit < 0:
            raise ValidationError(
                f"Invalid limit: {limit}. Must be a non-negative integer."
            )

    # Search type
    search_type = kwargs.get("type")
    if search_type is not None:
        allowed = ("track", "album")
        if search_type not in allowed:
            raise ValidationError(
                f"Invalid search type: '{search_type}'. "
                f"Allowed values: {', '.join(allowed)}"
            )
