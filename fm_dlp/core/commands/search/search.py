from collections.abc import Generator

from ...utils.colors import error, set_colors


class Search:
    """
    Handles searching across YouTube and YouTube Music with unified interface.

    This class acts as a facade that delegates to the appropriate provider
    (YouTubeProvider or YouTubeMusicProvider) based on the `yt_video` flag.
    It also handles error handling, color configuration, and result formatting.

    Features:
    - Search for videos, tracks, albums, or playlists
    - Support for raw output (Python dicts) or formatted strings
    - URL-only output for piping to downloaders
    - Graceful error handling with timeout detection
    - Color-coded output for better readability

    Args:
        query (str): The search query string.
        limit (int): Maximum number of results to return.
        yt_video (bool): If True, search YouTube videos; if False, search YouTube Music.
        album (bool): If True, search for albums/playlists; if False, search for tracks.
        raw (bool): If True, output raw Python dictionaries instead of formatted strings.
        only_url (bool): If True, output only URLs without any formatting.
        color (bool): If True, enable ANSI color codes in output.
    """

    def __init__(
        self,
        query: str,
        limit: int,
        yt_video: bool,
        album: bool,
        raw: bool,
        only_url: bool,
        color: bool,
    ):
        self.query = query
        self.limit = limit
        self.yt_video = yt_video
        self.raw = raw
        self.only_url = only_url
        self.is_track = not album
        self.color = color

        set_colors(color)

    def search(self) -> Generator[str, None, None] | str:
        """
        Perform search using the appropriate provider based on initialization flags.

        Delegates to:
        - YouTubeProvider if `yt_video` is True (searches YouTube videos/playlists)
        - YouTubeMusicProvider if `yt_video` is False (searches YouTube Music tracks/albums)

        Handles provider-specific exceptions:
        - For YouTube Music: catches timeout errors (ReadTimeout, ReadTimeoutError, TimeoutError)
          and returns a formatted timeout message
        - For YouTube: catches all exceptions and returns an empty string (silent failure)

        Returns:
            Generator[str, None, None] | str: A generator yielding search results,
                or an empty string if an error occurs with YouTube provider.
        """
        from .providers import YouTubeMusicProvider, YouTubeProvider

        yt_provider = YouTubeProvider(self.color)
        ytm_provider = YouTubeMusicProvider(self.color)

        if self.yt_video:
            try:
                yield from yt_provider.search(
                    self.query,
                    self.limit,
                    self.is_track,
                    self.raw,
                    self.only_url,
                )
            except Exception:
                return
        else:
            from requests.exceptions import ReadTimeout
            from urllib3.exceptions import ReadTimeoutError

            try:
                yield from ytm_provider.search(
                    self.query,
                    self.limit,
                    self.is_track,
                    self.raw,
                    self.only_url,
                )
            except (
                ReadTimeoutError,
                ReadTimeout,
                TimeoutError,
            ):
                yield error("Connection timeout")
            except Exception as e:
                yield error(str(e))
