"""Search providers for YouTube and YouTube Music."""

from abc import ABC, abstractmethod
from itertools import islice
from typing import Any, Dict, Generator, Optional

from fm_dlp.commands.search.formatters import ResultFormatter


class BaseProvider(ABC):
    """Abstract base class for search providers."""

    def __init__(self, formatter=ResultFormatter):
        self.formatter = formatter

    @abstractmethod
    def _build_search_query(self, query: str, limit: int, is_track: bool) -> str:
        """Build provider-specific search query."""
        pass

    @abstractmethod
    def _extract_results(self, query: str, limit: int, is_track: bool) -> list:
        """Extract search results from provider."""
        pass

    @abstractmethod
    def _format_entry(
        self, entry: Dict[str, Any], num: int, is_track: bool
    ) -> Optional[str]:
        """Format a single search entry."""
        pass

    @abstractmethod
    def _extract_url(self, entry: Dict[str, Any], is_track: bool) -> Optional[str]:
        """Extract URL from search entry."""
        pass

    @abstractmethod
    def _get_empty_message(self, query: str, is_track: bool) -> str:
        """Get message when no results found."""
        pass

    def search(
        self,
        query: str,
        limit: int,
        is_track: bool,
        raw: bool,
        only_url: bool,
    ) -> Generator[str, None, None]:
        """
        Generic search method that handles common logic.

        Args:
            query: Search query string
            limit: Maximum number of results
            is_track: True for tracks/videos, False for albums/playlists
            raw: Return raw data if True
            only_url: Return only URLs if True
        """
        try:
            results = self._extract_results(query, limit, is_track)

            if not results:
                if not only_url:
                    yield self._get_empty_message(query, is_track)
                return

            if raw:
                for entry in islice(results, limit):
                    yield str(entry) + "\n"
                return

            for num, entry in enumerate(islice(results, limit), 1):
                url = self._extract_url(entry, is_track)

                if not url:
                    continue

                if only_url:
                    yield url
                else:
                    formatted = self._format_entry(entry, num, is_track)
                    if formatted:
                        yield formatted

        except KeyboardInterrupt:
            return
        except Exception as e:
            yield self.formatter.format_error(f"Search Error: {e}")
            return


class YouTubeProvider(BaseProvider):
    """Search provider for YouTube videos and playlists."""

    @staticmethod
    def _ytdl_opts() -> dict:
        """Get yt-dlp options for YouTube extraction."""
        return {
            "quiet": True,
            "extract_flat": True,
            "cachedir": False,
            "extractor_args": {
                "youtube": {
                    "player_client": ["web", "ios"],
                    "player_skip": ["configs", "js", "webpage", "authcheck"],
                }
            },
        }

    def _build_search_query(self, query: str, limit: int, is_track: bool) -> str:
        search_type = "video" if is_track else "playlist"
        return f"ytsearch{limit}:{search_type}:{query}"

    def _extract_results(self, query: str, limit: int, is_track: bool) -> list:
        from yt_dlp import YoutubeDL

        with YoutubeDL(self._ytdl_opts()) as ydl:
            info = ydl.extract_info(
                self._build_search_query(query, limit, is_track), download=False
            )
            return info.get("entries", [])

    def _extract_url(self, entry: Dict[str, Any], is_track: bool) -> Optional[str]:
        if v_id := entry.get("id"):
            return "https://youtu.be/" + v_id
        return None

    def _format_entry(
        self, entry: Dict[str, Any], num: int, is_track: bool
    ) -> Optional[str]:
        return self.formatter.format_result(
            num,
            title=entry.get("title", "Unknown Video"),
            artist=entry.get("channel", "Unknown Channel"),
            url="https://youtu.be/" + entry.get("id", ""),
            is_yt_video=True,
            is_track=is_track,
            views=self.formatter.fmt_views(entry.get("view_count")),
            duration=self.formatter.fmt_duration(entry.get("duration")),
        )

    def _get_empty_message(self, query: str, is_track: bool) -> str:
        return f"No videos matching '{query}'\n"


class YouTubeMusicProvider(BaseProvider):
    """Search provider for YouTube Music tracks and albums."""

    def _build_search_query(self, query: str, limit: int, is_track: bool) -> str:
        return query

    def _extract_results(self, query: str, limit: int, is_track: bool) -> list:
        from ytmusicapi import YTMusic

        search_type = "songs" if is_track else "albums"
        return YTMusic().search(query=query, limit=limit, filter=search_type)

    def _extract_url(self, entry: Dict[str, Any], is_track: bool) -> Optional[str]:
        if is_track:
            if t_id := entry.get("videoId"):
                return "https://music.youtube.com/watch?v=" + t_id
        else:
            if pl_id := entry.get("playlistId"):
                return "https://music.youtube.com/playlist?list=" + pl_id
        return None

    def _format_entry(
        self, entry: Dict[str, Any], num: int, is_track: bool
    ) -> Optional[str]:
        if is_track:
            return self.formatter.format_result(
                num,
                title=entry.get("title", "Unknown Track"),
                artist=self.formatter.extract_artist(entry),
                album=entry.get("album", {}).get("name", "Unknown Album"),
                url="https://music.youtube.com/watch?v=" + entry.get("videoId", ""),
                is_yt_video=False,
                is_track=True,
                views=self.formatter.fmt_views(entry.get("views")),
                duration=self.formatter.fmt_duration(entry.get("duration")),
            )
        else:
            return self.formatter.format_result(
                num,
                title=entry.get("title", "Unknown Album"),
                artist=self.formatter.extract_artist(entry),
                url="https://music.youtube.com/playlist?list="
                + entry.get("playlistId", ""),
                is_yt_video=False,
                is_track=False,
                year=entry.get("year", "N/A"),
            )

    def _get_empty_message(self, query: str, is_track: bool) -> str:
        result_type = "tracks" if is_track else "albums"
        return f"No {result_type} found for '{query}'\n"
