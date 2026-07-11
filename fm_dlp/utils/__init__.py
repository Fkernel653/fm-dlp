import sys
from typing import TextIO

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


def echo(text: str, file: TextIO = sys.stdout) -> None:
    """Print message to file.

    Args:
        text: Message to print.
        file: File to write to (default: stdout).
    """
    file.write(text + "\n")
