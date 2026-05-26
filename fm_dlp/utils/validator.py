"""Input validation module for fm-dlp CLI application."""

import sys
from typing import Annotated, Literal, TypeAlias

from pydantic import BaseModel, Field, HttpUrl, field_validator

PROTOCOLS = ("http://", "https://", "socks4://", "socks5://", "socks5h://")
HTTP_PROTOCOLS = ("http://", "https://")
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
Platform: TypeAlias = Literal["yt-video", "yt-music"]


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


class DownloadParams(BaseModel):
    url: HttpUrl | None = None
    codec: Codec | None = None
    kbps: Annotated[int, Field(ge=64, le=320)] | None = None
    max_concurrent: Annotated[int, Field(ge=1)] | None = None
    limit: Annotated[int, Field(ge=0)] | None = None
    platform: Platform | None = None
    type: SearchType | None = None
    proxy: str | None = None
    proxy_only_http: bool = False

    @field_validator("proxy")
    @classmethod
    def validate_proxy(cls, v: str | None, info) -> str | None:
        if v is None:
            return None
        allowed = HTTP_PROTOCOLS if info.data.get("proxy_only_http") else PROTOCOLS
        if not v.startswith(allowed):
            raise ValueError(
                f"Invalid proxy URL: '{v}'. Allowed protocols: {', '.join(allowed)}"
            )
        return v


def validate_input(**kwargs) -> None:
    """Validate all CLI input parameters."""
    try:
        DownloadParams(**kwargs)
    except Exception as e:
        raise ValidationError(str(e)) from e
