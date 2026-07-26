"""Configuration handling for downloader."""

from typing import Any

from ...utils.config.configer.parametrs import get_parameters, set_parameters


class DownloadConfig:
    """Configuration container for download settings."""

    def __init__(
        self,
        url: str,
        codec: str,
        kbps: int,
        quality: str,
        jobs: int,
        quiet: bool,
        metadata: bool,
        keep: bool,
        save: bool,
        use_config: bool,
        path: str,
        only_video: bool,
        cookies: str | None,
        color: bool,
    ):
        self.url = url
        self.codec = codec
        self.kbps = kbps
        self.quality = quality
        self.jobs = jobs
        self.quiet = quiet
        self.metadata = metadata
        self.keep = keep
        self.save = save
        self.use_config = use_config
        self.path = path
        self.only_video = only_video
        self.cookies = cookies
        self.color = color

    def apply_config(self) -> dict[str, Any]:
        """Apply saved config if requested and return parameters dict."""
        if self.use_config:
            params = get_parameters(self.color)
            return {
                "codec": params.get("codec", self.codec),
                "kbps": params.get("kbps", self.kbps),
                "quality": params.get("quality", self.quality),
                "jobs": params.get("jobs", self.jobs),
                "quiet": params.get("quiet", self.quiet),
                "metadata": params.get("metadata", self.metadata),
                "keep": params.get("keep", self.keep),
                "only_video": params.get("only_video", self.only_video),
                "cookies": params.get("cookies", self.cookies),
            }
        return {
            "codec": self.codec,
            "kbps": self.kbps,
            "quality": self.quality,
            "jobs": self.jobs,
            "quiet": self.quiet,
            "metadata": self.metadata,
            "keep": self.keep,
            "only_video": self.only_video,
            "cookies": self.cookies,
        }

    def save_config(self) -> bool:
        """Save current settings to config file."""
        if self.save:
            return set_parameters(
                self.codec,
                self.kbps,
                self.quality,
                self.jobs,
                self.quiet,
                self.metadata,
                self.keep,
                self.only_video,
                self.cookies,
                self.color,
            )
        return True
