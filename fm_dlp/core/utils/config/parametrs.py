from typing import Any

from ...commands.downloader.params import DownloadParams
from ...utils import echo, echo_error, set_colors, success
from .config_manager import ConfigManager
from .params import ConfigParams


class ParametersManager:
    """
    Manage download parameters stored in the configuration file.

    This class provides methods to read and write the ``[parameters]``
    section of the application's TOML configuration. It handles codec,
    bitrate, quality, job count, and various boolean flags, as well as
    optional cookies and remote URL values.

    Attributes:
        params (ConfigParams): Configuration parameters (quiet, color, config_file).
        config_manager (ConfigManager): Underlying config manager.
        param_key (str): Config key for the parameters section.
    """

    def __init__(self, params: ConfigParams):
        self.params = params
        self.config_manager = ConfigManager(params)
        self.param_key = "parameters"
        set_colors(params.color)

    def set_parameters(self, params: DownloadParams) -> bool:
        """
        Write download parameters to the configuration file.

        Args:
            params (DownloadParams): Download parameters

        Returns:
            bool: True if the parameters were saved successfully, False otherwise.
        """
        try:
            config = self.config_manager.load_config()

            download_params: dict[str, Any] = {
                "codec": params.codec,
                "kbps": params.kbps,
                "quality": params.quality,
                "jobs": params.jobs,
                "quiet": params.quiet,
                "metadata": params.metadata,
                "keep": params.keep,
                "only_video": params.only_video,
                "subtitles": params.subtitles,
                "subtitle_langs": params.subtitle_langs,
                "embed_subs": params.embed_subs,
                "auto_subs": params.auto_subs,
            }

            if params.ffmpeg_path:
                download_params["ffmpeg_path"] = params.ffmpeg_path

            if params.cookies:
                download_params["cookies"] = params.cookies

            if params.remote:
                download_params["remote"] = params.remote

            config[self.param_key] = download_params

            if not self.config_manager.update_config(config):
                if not self.params.quiet:
                    echo_error(
                        f"Failed to write {self.config_manager.config_file}",
                    )
                return False

            if not self.params.quiet:
                echo(success("Parameters have been successfully saved"))

            return True

        except OSError as e:
            if not self.params.quiet:
                echo_error(f"Failed to save configuration: {e}")
            return False

    def get_parameters(self) -> dict[str, Any]:
        """
        Retrieve download parameters from the configuration file.

        Returns:
            dict[str, Any]: A dictionary of stored parameters, or an empty
            dictionary if the configuration file does not exist or contains
            no parameters section.
        """
        if not self.config_manager.config_file.exists():
            return {}

        config = self.config_manager.load_config()
        return config.get(self.param_key, {})
