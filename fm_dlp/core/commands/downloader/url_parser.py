from pathlib import Path

from ...utils import echo, echo_error, info


class URLParser:
    """Parse URLs from string or file."""

    def __init__(self, urls: str, quiet: bool):
        self.urls = urls
        self.quiet = quiet

    def parse(self) -> list[str]:
        """Parse URLs from string or file path."""
        if not self.urls:
            return []

        url_path = Path(self.urls)
        if url_path.is_file():
            return self._parse_url_file(url_path)

        return [u.strip() for u in self.urls.replace(",", " ").split() if u.strip()]

    def _parse_url_file(self, file_path: Path) -> list[str]:
        urls_from_file: list[str] = []

        try:
            content = file_path.read_text(encoding="utf-8")
            for line in content.splitlines():
                line = str(line.strip())
                if line and not line.startswith("#"):
                    urls_from_file.extend(
                        u.strip() for u in line.replace(",", " ").split() if u.strip()
                    )

            if not self.quiet:
                echo(info(f"Loaded {len(urls_from_file)} URLs from file: {self.urls}"))

        except UnicodeDecodeError:
            echo_error(
                f"File '{self.urls}' is not UTF-8 encoded. Please save it as UTF-8."
            )

        except FileNotFoundError:
            echo_error(f"File not found: '{self.urls}'")

        except PermissionError:
            echo_error(f"Permission denied: Cannot read file '{self.urls}'")

        except IsADirectoryError:
            echo_error(f"Path is a directory, not a file: '{self.urls}'")

        except OSError as e:
            echo_error(f"Error reading URL file: {e}")

        return urls_from_file
