"""Input validation module for fm-dlp CLI application."""

import sys
from typing import Any, Literal, TypeAlias
from urllib.parse import urlparse

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


def _validate_url_string(url: str) -> str:
    """Validate a URL string has proper format."""
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError
        if parsed.scheme not in ("http", "https"):
            raise ValidationError(
                f"Invalid URL protocol: '{parsed.scheme}://'. "
                f"Only http:// and https:// are allowed."
            )
    except ValueError:
        raise ValidationError(
            f"Invalid URL: '{url}'. Must be a valid HTTP(S) URL with domain."
        )
    return url


def _validate_proxy_string(proxy: str, http_only: bool = False) -> str:
    """Validate a proxy URL string."""
    try:
        parsed = urlparse(proxy)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError

        allowed = (
            ("http", "https")
            if http_only
            else ("http", "https", "socks4", "socks5", "socks5h")
        )
        if parsed.scheme not in allowed:
            raise ValidationError(
                f"Invalid proxy protocol: '{parsed.scheme}://'. "
                f"Allowed protocols: {', '.join(p + '://' for p in allowed)}"
            )
    except ValueError:
        allowed = HTTP_PROTOCOLS if http_only else PROTOCOLS
        raise ValidationError(
            f"Invalid proxy URL: '{proxy}'. Allowed protocols: {', '.join(allowed)}"
        )
    return proxy


def validate_input(**kwargs: Any) -> None:
    """Validate all CLI input parameters.

    Args:
        **kwargs: Input parameters to validate.

    Raises:
        ValidationError: If any parameter fails validation.
    """
    # URL
    url = kwargs.get("url")
    if url is not None:
        _validate_url_string(str(url))

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

    # Max concurrent
    max_concurrent = kwargs.get("max_concurrent")
    if max_concurrent is not None:
        if not isinstance(max_concurrent, int) or max_concurrent < 1:
            raise ValidationError(
                f"Invalid max_concurrent: {max_concurrent}. Must be an integer >= 1."
            )

    # Limit
    limit = kwargs.get("limit")
    if limit is not None:
        if not isinstance(limit, int) or limit < 0:
            raise ValidationError(
                f"Invalid limit: {limit}. Must be a non-negative integer."
            )

    # Platform
    platform = kwargs.get("platform")
    if platform is not None:
        allowed = ("yt-video", "yt-music")
        if platform not in allowed:
            raise ValidationError(
                f"Invalid platform: '{platform}'. Allowed values: {', '.join(allowed)}"
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

    # Proxy
    proxy = kwargs.get("proxy")
    if proxy is not None:
        proxy_only_http = kwargs.get("proxy_only_http", False)
        _validate_proxy_string(str(proxy), http_only=proxy_only_http)
