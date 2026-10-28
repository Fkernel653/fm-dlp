from ...utils.colors import BOLD_CYAN, BOLD_RED, BOLD_WHITE, GRAY, RESET


class ResultFormatter:
    """Format search results with optional metadata and colors."""

    def __init__(self, color: bool):
        """Initialize formatter with color settings."""
        self.color = color
        self._c = {
            "bc": BOLD_CYAN if color else "",
            "br": BOLD_RED if color else "",
            "bw": BOLD_WHITE if color else "",
            "g": GRAY if color else "",
            "w": "\033[0;37m" if color else "",
            "r": RESET if color else "",
        }

    @staticmethod
    def fmt_views(v: str | int | None) -> str:
        """
        Format view count with thousands separators (commas).

        Handles various input types commonly returned by YouTube APIs:
        - Integer values are formatted with commas (e.g., 1234567 → "1,234,567")
        - String values are returned as-is (already formatted)
        - None values return "N/A" for missing data

        Args:
            v (str | int | None): The view count value to format.

        Returns:
            str: Formatted view count string with commas or "N/A" if not available.
        """
        if v is None:
            return "N/A"

        if isinstance(v, str):
            return v

        return f"{int(float(v)):,}"

    @staticmethod
    def fmt_duration(d: str | float | None) -> str:
        """
        Format duration from seconds to human-readable MM:SS or HH:MM:SS.

        Converts a duration value (in seconds) to a standardized time format:
        - If duration < 1 hour → returns as MM:SS (e.g., "3:45")
        - If duration >= 1 hour → returns as HH:MM:SS (e.g., "1:23:45")
        - If input is already formatted (contains ":") → returns as-is
        - None values return "N/A"

        Args:
            d (str | float | None): Duration in seconds or pre-formatted string.

        Returns:
            str: Formatted duration string or "N/A" if not available.
        """
        if d is None:
            return "N/A"

        d_str = str(d)
        if ":" in d_str:
            return d_str

        s = int(d)
        h, remainder = divmod(s, 3600)
        m, s = divmod(remainder, 60)

        return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

    @staticmethod
    def extract_artist(item: dict[str, list[str]]) -> str:
        """
        Extract artist name from a YouTube Music API response item.

        Parses the nested "artists" structure commonly found in ytmusicapi responses.
        If the artist list exists and is non-empty, returns the first artist's name;
        otherwise returns "Unknown Artist" as a fallback.

        Args:
            item (dict): A search result item from YouTube Music API.

        Returns:
            str: The artist name or "Unknown Artist" if not found.
        """
        artists = item.get("artists", [])
        return artists[0].get("name", "N/A")

    def fmt_result(
        self,
        num: int,
        title: str,
        artist: str,
        url: str,
        is_yt_video: bool,
        is_track: bool,
        **kwargs: str | dict[str, str | int | float],
    ) -> str:
        """
        Format a single search result with a structured tree-like layout.

        Creates a visually organized output with:
        - A numbered header with the result title
        - Hierarchical indentation using tree symbols (├─, └─, │)
        - Color-coded elements (cyan for numbers, white for details, gray for tree lines)
        - Different metadata layouts depending on result type:
            * YouTube videos: artist, views, duration
            * YouTube Music tracks: artist, album, views, duration
            * Albums/playlists: artist, year
        - A red URL at the bottom if available
        - A separator line after each result

        Args:
            num (int): Result number/index.
            title (str): Title of the video/track/album.
            artist (str): Artist or channel name.
            url (str): URL to the content.
            is_yt_video (bool): True for YouTube videos, False for YouTube Music results.
            is_track (bool): True for tracks/videos, False for albums/playlists.
            **kwargs: Additional metadata (views, duration, album, year).

        Returns:
            str: A formatted multi-line string representing the search result.
        """
        c = self._c
        w = c["w"]
        g = c["g"]

        tree = f"    {g}├─"
        corner = f"    {g}└─"
        sep = f" {g}│{w} "
        div = f"       {g}{'─' * 50}{c['r']}\n"

        lines = [f"\n{c['bc']}{num}. {c['bw']}{title}"]

        views = str(kwargs.get("views", "N/A"))
        duration = str(kwargs.get("duration", "N/A"))

        if is_yt_video:
            lines.append(f"{tree} {w + artist}")
            lines.append(f"{tree} {w + views}{sep}{w + duration}")

        elif is_track:
            album = str(kwargs.get("album", "N/A"))
            lines.extend(
                [
                    f"{tree} {w + album}",
                    f"{tree} {w + artist}",
                    f"{tree} {w + views}{sep}{w + duration}",
                ]
            )

        else:
            year = str(kwargs.get("year", "N/A"))
            lines.extend([f"{tree} {w + artist}", f"{tree} {w + year}"])

        lines.append(f"{corner} {c['br']}{url}")
        lines.append(div)

        return "\n".join(lines)
