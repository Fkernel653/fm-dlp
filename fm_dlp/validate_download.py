"""Provide input validation for the 'download' command in the fm-dlp CLI application."""

from functools import lru_cache
from pathlib import Path

from fm_dlp_core.utils import echo, sys
from fm_dlp_core.utils.colors import error, hint, set_colors


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


class ValidateDownload:
    """Validator for download parameters."""

    def __init__(
        self,
        url: str,
        quality: str,
        path: str,
        cookies: str | None = None,
        color: bool = True,
    ) -> None:
        """Initialize validator with all download parameters."""
        self.url = url
        self.quality = quality
        self.path = path
        self.cookies = cookies
        self.color = color

        set_colors(color)

    def _validate_url(self) -> None:
        """Validate URL or file path."""
        path = Path(self.url)

        if path.exists():
            _check(
                path.is_file(),
                f"Path exists but is not a file: '{self.url}'",
                "Must be a URL (http:// or https://) or a path to a text file containing URLs",
            )
            _check(
                path.stat().st_size > 0,
                f"URL file is empty: '{self.url}'",
            )
            return

        _check(
            self.url.startswith(("http://", "https://")) and len(self.url) > 7,
            f"Invalid URL or file: '{self.url}'",
            "Must start with 'http://' or 'https://' and contain a valid address",
        )

    def _validate_quality(self) -> None:
        """Validate video quality parameter."""
        quality = self.quality
        if quality.isdigit():
            quality = f"{quality}p"

        SUPPORTED_QUALITES = {
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
            "2160",
            "1440",
            "1080",
            "720",
            "480",
            "360",
            "240",
            "144",
        }

        if quality in SUPPORTED_QUALITES:
            return

        _fail(
            f"Unusual quality format '{quality}'. yt-dlp will attempt to handle it.",
            f"Allowed formats: {', '.join(SUPPORTED_QUALITES)}",
        )

    def _validate_path(self) -> None:
        """Validate download directory path."""
        real_path = Path(self.path)

        _check(
            not real_path.is_file(),
            "The path must not be a file",
            "Enter the path to the folder",
        )

        _check(
            not (real_path.exists() and not real_path.is_dir()),
            f"Path exists but is not a directory: '{self.path}'",
            "Enter a valid directory path",
        )

        parent = real_path.parent
        _check(
            not (parent.exists() and not parent.is_dir()),
            f"Parent path is not a directory: '{parent}'",
        )

    def _validate_cookies(self) -> None:
        """Validate cookies parameter (browser name or file path)."""
        if self.cookies is None:
            return

        _check(
            bool(self.cookies),
            "Cookies parameter cannot be empty",
            "Provide a browser name or path to cookie file",
        )

        cookies_path = Path(self.cookies)

        if cookies_path.exists():
            _check(
                cookies_path.is_file(),
                f"Path exists but is not a file: '{self.cookies}'",
                "Must be a path to a cookie file",
            )
            COOKIE_EXTENSIONS = {".txt", ".sqlite", ".db", ".cookies"}
            _check(
                cookies_path.suffix.lower() in COOKIE_EXTENSIONS,
                f"Cookie file has unusual extension: '{cookies_path.suffix}'",
                f"Supported extensions: {', '.join(COOKIE_EXTENSIONS)}",
            )
            _check(
                cookies_path.stat().st_size > 0,
                f"Cookie file is empty: '{self.cookies}'",
            )
        else:
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

            _check(
                self.cookies.lower() in SUPPORTED_BROWSERS,
                f"Unsupported browser: '{self.cookies}'",
                f"Supported browsers: {', '.join(sorted(SUPPORTED_BROWSERS))}. Or provide a path to a cookie file",
            )

    @staticmethod
    @lru_cache(maxsize=1)
    def _validate_ffmpeg() -> None:
        """Verify FFmpeg is installed."""
        import shutil

        _check(
            shutil.which("ffmpeg") is not None,
            "FFmpeg is not installed or not found in system PATH!",
            "Install FFmpeg and ensure it's accessible from the command line.",
        )

    def validate(self) -> None:
        """Validate all download parameters."""
        self._validate_url()
        self._validate_quality()
        self._validate_path()
        self._validate_cookies()
        self._validate_ffmpeg()
