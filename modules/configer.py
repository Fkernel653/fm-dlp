"""
Persistent download path storage using JSON config file.
"""

from json import dump
from pathlib import Path

from modules.colors import BLUE, GREEN, RED, RESET, YELLOW


def configer(path: str) -> str:
    """
    Manage download directory storage.
    - With path: saves to config.json
    - Without path: displays current config
    """
    config_file = Path(__file__).parent.parent / "config.json"

    try:
        input_path = Path(path).expanduser().resolve()
        if not input_path.exists():
            return f"{RED}Please enter the correct path!{RESET}"

        config = {"path": str(input_path)}
        with open(config_file, "w", encoding="utf-8") as f:
            dump(config, f, ensure_ascii=False, indent=4)

        return (
            f"{GREEN}Configuration saved successfully!{RESET}\n"
            f"{YELLOW}Path: {RESET}{input_path}\n"
            f"{BLUE}Config file: {RESET}{config_file}"
        )
    except Exception as e:
        return f"{RED}Error saving configuration: {e}{RESET}"
