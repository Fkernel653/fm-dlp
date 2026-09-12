import os
import sys

from fm_dlp_core.utils import echo, echo_error, info, set_colors


class ValidateDownload:
    """Validator for download parameters."""

    def __init__(
        self,
        url: str,
        quality: str,
        path: str,
        cookies: str | None,
        color: bool,
    ) -> None:
        self.url = url
        self.quality = quality
        self.path = path
        self.cookies = cookies
        self.color = color

        set_colors(color)

    def _validate_url(self) -> None:
        """Validate URL or file path."""
        if self.url.startswith(("http://", "https://")):
            self._check(
                len(self.url) > 7,
                f"Invalid URL: '{self.url}'",
                "Must start with 'http://' or 'https://' and contain a valid address",
            )
            return

        if os.path.exists(self.url):
            self._check(
                os.path.isfile(self.url),
                f"Path exists but is not a file: '{self.url}'",
                "Must be a URL (http:// or https://) or a path to a text file containing URLs",
            )
            self._check(
                os.path.getsize(self.url) > 0,
                f"URL file is empty: '{self.url}'",
            )
            return

        self._fail(
            f"Invalid URL or file: '{self.url}'",
            "Must start with 'http://' or 'https://' and contain a valid address",
        )

    def _validate_quality(self) -> None:
        """Validate video quality parameter."""
        quality = self.quality
        if quality.isdigit():
            quality = f"{quality}p"

        SUPPORTED_QUALITIES = (
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
        )

        if quality in SUPPORTED_QUALITIES:
            return

        self._fail(
            f"Unusual quality format '{quality}'. yt-dlp will attempt to handle it.",
            f"Allowed formats: {', '.join(SUPPORTED_QUALITIES)}",
        )

    def _validate_path(self) -> None:
        """Validate download directory path."""
        self._check(
            not os.path.isfile(self.path),
            "The path must not be a file",
            "Enter the path to the folder",
        )

        self._check(
            os.path.isdir(self.path),
            f"Path exists but is not a directory: '{self.path}'",
            "Enter a valid directory path",
        )

    def _validate_cookies(self) -> None:
        """Validate cookies parameter (browser name or file path)."""
        if self.cookies is None:
            return
        self._check(
            bool(self.cookies),
            "Cookies parameter cannot be empty",
            "Provide a browser name or path to cookie file",
        )

        SUPPORTED_BROWSERS = (
            "brave",
            "chrome",
            "chromium",
            "edge",
            "opera",
            "vivaldi",
            "whale",
            "firefox",
            "safari",
        )

        if self.cookies.lower() in SUPPORTED_BROWSERS:
            return

        if os.path.exists(self.cookies):
            self._check(
                os.path.isfile(self.cookies),
                f"Path exists but is not a file: '{self.cookies}'",
                "Must be a path to a cookie file",
            )

            COOKIE_EXTENSIONS = (".txt", ".sqlite", ".db", ".cookies")

            _, ext = os.path.splitext(self.cookies)
            self._check(
                ext.lower() in COOKIE_EXTENSIONS,
                f"Cookie file has unusual extension: '{ext}'",
                f"Supported extensions: {', '.join(COOKIE_EXTENSIONS)}",
            )
            self._check(
                os.path.getsize(self.cookies) > 0,
                f"Cookie file is empty: '{self.cookies}'",
            )
            return

        self._fail(
            f"Unsupported browser or missing cookie file: '{self.cookies}'",
            f"Supported browsers: {', '.join(sorted(SUPPORTED_BROWSERS))}. "
            f"Or provide a path to a cookie file",
        )

    def _validate_ffmpeg(self) -> None:
        """Verify FFmpeg is installed."""
        import shutil

        self._check(
            shutil.which("ffmpeg") is not None,
            "FFmpeg is not installed or not found in system PATH!",
            "Install FFmpeg and ensure it's accessible from the command line.",
        )

    def _fail(self, msg: str, tip: str | None = None) -> None:
        """Print error message and exit."""
        echo_error(msg, exit=False)
        if tip:
            echo(info(tip))
        sys.exit(1)

    def _check(self, condition: bool, msg: str, tip: str | None = None) -> None:
        """Check condition and exit with error if not met."""
        if not condition:
            self._fail(msg, tip)

    def validate(self) -> None:
        """Validate all download parameters."""
        self._validate_quality()
        self._validate_path()
        self._validate_cookies()
        self._validate_url()
        self._validate_ffmpeg()
