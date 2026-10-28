from pathlib import Path

from ...utils import echo, echo_error, set_colors, success
from .config_manager import ConfigManager
from .params import ConfigParams


class PathManager:
    """
    Manage the download path stored in the configuration file.

    This class provides methods to read and write the ``path`` key of the
    application's TOML configuration. When no configuration file exists,
    the user's home directory is used as a fallback.

    Attributes:
        params (ConfigParams): Configuration parameters (quiet, color, config_file).
        config_manager (ConfigManager): Underlying config manager.
        path_key (str): Config key for the download path.
    """

    def __init__(self, params: ConfigParams):
        self.params = params
        self.config_manager = ConfigManager(params)
        self.path_key = "path"
        set_colors(params.color)

    def set_path(self, path: str) -> None:
        """
        Validate and save the download path to the configuration file.

        Args:
            path (str): The path to the download directory. Tilde (``~``) is expanded.

        Returns:
            None
        """
        try:
            input_path = str(Path(path).expanduser().resolve())

            if not Path(input_path).is_dir():
                if not self.params.quiet:
                    echo_error("Please enter the correct path!")
                return

            config = self.config_manager.load_config()
            config[self.path_key] = input_path

            if not self.config_manager.update_config(config):
                if not self.params.quiet:
                    echo_error(f"Failed to write {self.config_manager.config_file}")
                return

            if not self.params.quiet:
                echo(success("Configuration saved successfully"))

        except OSError as e:
            if not self.params.quiet:
                echo_error(f"Failed to save configuration: {e}")

    def get_path(self) -> str:
        """
        Retrieve the download path from the configuration file.

        If no configuration file exists, the user's home directory is returned
        along with an informational hint. If the stored path is missing or no
        longer a valid directory, an error message is shown and the home
        directory is returned as a fallback.

        Returns:
            str: The resolved download directory path.
        """
        if not self.config_manager.config_file.exists():
            if not self.params.quiet:
                echo_error("Failed to find configuration file. Home directory is used!")
            return str(Path.home())

        data = self.config_manager.load_config()
        download_path = data.get(self.path_key)

        if not download_path or not Path(str(download_path)).is_dir():
            if not self.params.quiet:
                echo_error("Failed to find download path. Home directory is used!")
            return str(Path.home())

        return str(download_path)
