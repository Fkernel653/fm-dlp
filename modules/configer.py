"""
Persistent download path storage using JSON config file.
"""

from json import JSONDecodeError, dump, load
from pathlib import Path

from modules.colors import BLUE, GREEN, RED, RESET, YELLOW


def configer(path: str) -> str:
    """
    Manage download directory storage.
    - With path: saves to config.json
    - Without path: displays current config
    """
    config_file = Path(__file__).parent.parent / "config.json"

    # Setter mode
    if path:
        try:
            input_path = Path(path).expanduser().resolve()

            config = {"path": str(input_path)}
            with open(config_file, "w", encoding="utf-8") as f:
                dump(config, f, ensure_ascii=False, indent=4)

            return (
                f"{GREEN}Configuration saved successfully!{RESET}\n"
                f"{YELLOW}    Path: {RESET}{input_path}\n"
                f"{BLUE}    Config file: {RESET}{config_file}"
            )

        except Exception as e:
            return f"{RED}Error saving configuration: {e}{RESET}"

    # Getter mode
    else:
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    data = load(f)
                    saved_path_str = data.get("path")

                    if saved_path_str:
                        saved_path = Path(saved_path_str)

                        if saved_path.exists():
                            return (
                                f"{GREEN}Current download directory: {RESET}{saved_path}\n"
                                f"{BLUE}Configuration file: {RESET}{config_file}"
                            )
                        else:
                            return (
                                f"{RED}Config file exists but the saved path is invalid!{RESET}\n"
                                f"{RED}    Path: {RESET}{saved_path}"
                            )
                    else:
                        return (
                            f"{RED}Config file exists but 'path' key is missing!{RESET}"
                        )

            except JSONDecodeError:
                return f"{RED}Config file is corrupted! Please reconfigure with 'config <path>'.{RESET}"
            except Exception as e:
                return f"{RED}Error reading configuration: {e}{RESET}"
        else:
            return f"{RED}Config file not found! Please set a download path first with 'config <path>'.{RESET}"
