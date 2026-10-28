from typing import Any

from ...utils.config import ConfigParams, ParametersManager
from .params import DownloadParams


class DownloadConfig:
    """Configuration container for download settings."""

    def __init__(self, params: DownloadParams):
        self.params = params
        self.params_manager = ParametersManager(
            ConfigParams(params.quiet, params.color, params.config_file)
        )

    def apply_config(self) -> dict[str, Any]:
        """
        Apply saved configuration settings if requested and return parameters dict.

        If `use_config` is True, this method retrieves previously saved parameters
        from the configuration storage and merges them with the current instance
        values, giving priority to saved values. If `use_config` is False or no
        saved configuration exists, the current instance values are returned unchanged.

        Returns:
            dict[str, Any]: A dictionary containing the final parameters to be used
                for downloading. Keys include: codec, kbps, quality, jobs, quiet,
                metadata, keep, only_video, cookies, remote, subtitles,
                subtitle_langs, embed_subs, auto_subs, ytdlp_args.
        """
        if self.params.use_config:
            conf = self.params_manager.get_parameters()
            return {
                "codec": conf.get("codec", self.params.codec),
                "kbps": conf.get("kbps", self.params.kbps),
                "quality": conf.get("quality", self.params.quality),
                "jobs": conf.get("jobs", self.params.jobs),
                "quiet": conf.get("quiet", self.params.quiet),
                "metadata": conf.get("metadata", self.params.metadata),
                "keep": conf.get("keep", self.params.keep),
                "ffmpeg_path": conf.get("ffmpeg_path", self.params.ffmpeg_path),
                "only_video": conf.get("only_video", self.params.only_video),
                "cookies": conf.get("cookies", self.params.cookies),
                "remote": conf.get("remote", self.params.remote),
                "subtitles": conf.get("subtitles", self.params.subtitles),
                "subtitle_langs": conf.get(
                    "subtitle_langs", self.params.subtitle_langs
                ),
                "embed_subs": conf.get("embed_subs", self.params.embed_subs),
                "auto_subs": conf.get("auto_subs", self.params.auto_subs),
                "ytdlp_args": conf.get("ytdlp_args", self.params.ytdlp_args),
            }
        return {
            "codec": self.params.codec,
            "kbps": self.params.kbps,
            "quality": self.params.quality,
            "jobs": self.params.jobs,
            "quiet": self.params.quiet,
            "metadata": self.params.metadata,
            "keep": self.params.keep,
            "ffmpeg_path": self.params.ffmpeg_path,
            "only_video": self.params.only_video,
            "cookies": self.params.cookies,
            "remote": self.params.remote,
            "subtitles": self.params.subtitles,
            "subtitle_langs": self.params.subtitle_langs,
            "embed_subs": self.params.embed_subs,
            "auto_subs": self.params.auto_subs,
            "ytdlp_args": self.params.ytdlp_args,
        }

    def save_config(self) -> None:
        """
        Save current download settings to the persistent configuration file.

        This method persists the current instance parameters (codec, quality, jobs,
        subtitles, etc.) to the user's configuration storage so they can be reused
        in future sessions via the `--use-config` option. The method is only executed
        if the `save` flag is True.

        Returns:
            bool: True if configuration was saved successfully or if `save` is False
                (no operation needed), False if an error occurred during saving.
        """
        if self.params.save:
            self.params_manager.set_parameters(self.params)
