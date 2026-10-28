from dataclasses import dataclass


@dataclass
class ConfigParams:
    """
    Data container for shared configuration parameters.

    Aggregates common settings used across config managers: console output
    verbosity, colored output, and the path to the configuration file.
    All fields have defaults, so instances can be created without arguments.

    Attributes:
        quiet: Suppress console output if True.
        color: Enable colored console output if True.
        config_file: Custom path to the TOML config file. If None, the platform-specific default is used.
    """

    quiet: bool = False
    color: bool = True
    config_file: str | None = None
