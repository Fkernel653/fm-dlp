"""
Persistent download path storage using JSON config file.
"""

from json import JSONDecodeError, dump, load
from pathlib import Path

from modules.colors import GREEN, RED, RESET


def configer(path: str) -> str:
    """
    Manage download directory storage.
    - With path: saves to config.json
    - Without path: displays current config
    """
    config_file = Path(__file__).parent.parent / "config.json"

    # Setter mode
    if path:
        config = {"path": str(path)}
        with open(config_file, "w", encoding="utf-8") as f:
            dump(config, f, ensure_ascii=False, indent=4)
        return f"{GREEN}Configuration saved successfully to: {RESET}{Path(config_file)}"

    # Getter mode
    else:
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                try:
                    data = load(f)
                    saved_path = data.get("path")
                    if saved_path and Path(saved_path).exists():
                        return (
                            f"{GREEN}Current download directory: {RESET}{saved_path}\n"
                            f"{GREEN}Configuration file: {RESET}{Path(config_file)}"
                        )
                    else:
                        return f"{RED}\nConfig file exists but the saved path is invalid or missing!\n{RESET}"
                except JSONDecodeError:
                    return f"{RED}\nConfig file is corrupted! Please reconfigure with 'config <path>'.\n{RESET}"
        else:
            return f"{RED}\nConfig file not found! Please set a download path first with 'config <path>'.\n{RESET}"
