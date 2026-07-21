import sys
from typing import TextIO

AUDIO_CODECS = {"mp3", "aac", "flac", "m4a", "opus", "vorbis", "wav", "alac"}
VIDEO_CONTAINERS = {"mp4", "mov", "mkv", "webm", "avi", "flv"}
ALL_CODECS = AUDIO_CODECS | VIDEO_CONTAINERS
VIDEO_CONTAINER_AUDIO_MAP = {
    "mp4": "m4a",
    "mov": "m4a",
    "mkv": "opus",
    "webm": "opus",
    "avi": "mp3",
    "flv": "aac",
}
SUPPORTED_QUALITIES = {
    "best",
    "worst",
    "2160p",
    "1440p",
    "1080p",
    "720p",
    "480p",
    "360p",
    "240p",
    "144p",
}
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


def echo(text: str, file: TextIO = sys.stdout) -> None:
    """Print message to file.

    Args:
        text: Message to print.
        file: File to write to (default: stdout).
    """
    file.write(text + "\n")


def get_output(result: str) -> TextIO:
    """Determine output stream based on result content.

    Args:
        result: String to check for error indicators.

    Returns:
        sys.stderr if "Error" is found in result, otherwise sys.stdout.
    """
    return sys.stderr if "Error" in result else sys.stdout
