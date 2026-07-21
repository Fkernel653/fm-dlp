"""URL parsing utilities."""

import sys
from typing import List

from ...utils import echo
from ...utils.colors import error, info
from ...utils.config.path import Path


class URLParser:
    """Parse URLs from string or file."""

    def __init__(self, urls: str, quiet: bool):
        self.urls = urls
        self.quiet = quiet

    def parse(self) -> List[str]:
        """Parse URLs from string or file path."""
        if not self.urls:
            return []

        url_path = Path(self.urls)
        if url_path.is_file():
            return self._parse_url_file(url_path)

        return [u.strip() for u in self.urls.replace(",", " ").split() if u.strip()]

    def _parse_url_file(self, file_path: Path) -> List[str]:
        """Read and parse URLs from a text file (one URL per line)."""
        urls_from_file = []

        try:
            content = file_path.read_text(encoding="utf-8")
            for line in content.splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    urls_from_file.extend(
                        u.strip() for u in line.replace(",", " ").split() if u.strip()
                    )

            if not self.quiet:
                echo(info(f"Loaded {len(urls_from_file)} URLs from file: {self.urls}"))

        except UnicodeDecodeError:
            echo(
                error(
                    f"File '{self.urls}' is not UTF-8 encoded. Please save it as UTF-8.",
                ),
                file=sys.stderr,
            )
            sys.exit(1)

        except Exception as e:
            echo(error(f"Error reading URL file: {e}"), file=sys.stderr)
            sys.exit(1)

        return urls_from_file
