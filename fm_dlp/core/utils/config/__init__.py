"""
Configuration management for fm-dlp using persistent TOML storage.

This module handles reading, writing, and managing application configuration
including download paths and download parameters. Configuration is stored
in a platform-specific user config directory:

- Windows: %LOCALAPPDATA%\\fm-dlp\\config.toml
- macOS: ~/Library/Application Support/fm-dlp/config.toml
- Linux: $XDG_CONFIG_HOME/fm-dlp/config.toml or ~/.config/fm-dlp/config.toml

Submodules:
    config_manager: Core configuration management including file I/O and TOML serialization.
    parametrs: Parameter management for download configurations.
    path: Path management for download directories.

Constants:
    CONFIG_FILE: The path to the configuration file.

Classes:
    ConfigManager: Loads and updates the TOML configuration file with caching.
    СonfigParams: Shared configuration parameters for config managers.
    ParametersManager: Reads and writes download parameters in the config.
    PathManager: Reads and writes the download path in the config.
    TOMLSerializer: Serializes Python dictionaries to TOML format.

Example:
    >>> from fm_dlp_core.utils.config import ConfigManager, ConfigParams, PathManager
    >>> params = ConfigParams(color=True)
    >>> manager = ConfigManager(params)
    >>> config = manager.load_config()
    >>> config["path"] = "/downloads"
    >>> manager.update_config(config)
    True
    >>> path_manager = PathManager(params)
    >>> path_manager.get_path()
    '/downloads'
"""

from .config_manager import CONFIG_FILE, ConfigManager, TOMLSerializer
from .parametrs import ParametersManager
from .params import ConfigParams
from .path import PathManager

__all__ = [
    "CONFIG_FILE",
    "ConfigManager",
    "ConfigParams",
    "ParametersManager",
    "PathManager",
    "TOMLSerializer",
]
