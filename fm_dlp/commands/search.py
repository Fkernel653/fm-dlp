"""YouTube search handlers."""

from typing import Any, Generator

from fm_dlp.utils.colors import (
    BOLD,
    BOLD_CYAN,
    BOLD_RED,
    GRAY,
    RESET,
    error,
    set_colors,
    styled,
)


class Search:
    """Handles searching across YouTube and YouTube Music."""

    def __init__(
        self,
        query: str,
        limit: int,
        yt_video: bool,
        album: bool,
        raw: bool,
        only_url: bool,
        no_color: bool = False,
    ):
        """Initialize search with query parameters.

        Args:
            query: Search query string.
            limit: Maximum number of results.
            yt_video: Search YouTube videos instead of YouTube Music.
            album: Search for albums instead of tracks.
            raw: Output raw Python dicts instead of formatted strings.
            only_url: Output only URLs without formatting.
            no_color: Disable colored output.
        """
        self.query = query
        self.limit = limit
        self.yt_video = yt_video
        self.raw = raw
        self.only_url = only_url
        self.type = "album" if album else "track"
        self._is_track = self.type == "track"

        if no_color:
            set_colors(False)

        self._c = {
            "bold": BOLD if not no_color else "",
            "bold_cyan": BOLD_CYAN if not no_color else "",
            "bold_red": BOLD_RED if not no_color else "",
            "gray": GRAY if not no_color else "",
            "reset": RESET if not no_color else "",
        }

    @staticmethod
    def _fmt_views(v: Any) -> str:
        """Format view count with commas."""
        if v is None:
            return "N/A"
        try:
            return f"{int(float(v)):,}"
        except (ValueError, TypeError):
            return str(v)

    @staticmethod
    def _fmt_duration(d: Any) -> str:
        """Format duration from seconds to MM:SS or HH:MM:SS."""
        if d is None:
            return "N/A"
        d_str = str(d)
        if ":" in d_str:
            return d_str

        try:
            s = int(float(d)) if d else 0
            h, remainder = divmod(s, 3600)
            m, s = divmod(remainder, 60)
            return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
        except (ValueError, TypeError):
            return d_str

    @staticmethod
    def _extract_artist(item: dict) -> str:
        """Extract artist name from YouTube Music response."""
        artists = item.get("artists", [])
        return artists[0].get("name", "Unknown Artist") if artists else "Unknown Artist"

    def _format_result(
        self, num: int, title: str, artist: str, url: str, **kwargs
    ) -> str:
        """Format a single search result with optional metadata."""
        if self.only_url:
            return url

        c = self._c
        tree = f"    {c['gray']}├─{c['reset']}"
        corner = f"    {c['gray']}└─{c['reset']}"
        sep = f" {c['gray']}│{c['reset']} "
        div = f"       {c['gray']}{'─' * 50}{c['reset']}\n"

        lines = [f"\n{c['bold_cyan']}{num}. {c['reset']}{c['bold']}{title}{c['reset']}"]

        if self.yt_video:
            lines.append(f"{tree} {artist}")
            if self._is_track:
                lines.append(
                    f"{tree} {kwargs.get('views', 'N/A')}{sep}{kwargs.get('duration', 'N/A')}"
                )
        elif self._is_track:
            lines.extend(
                [f"{tree} {artist}", f"{tree} {kwargs.get('album', 'Unknown Album')}"]
            )
            lines.append(
                f"{tree} {kwargs.get('views', 'N/A')}{sep}{kwargs.get('duration', 'N/A')}"
            )
        else:
            lines.extend([f"{tree} {artist}", f"{tree} {kwargs.get('year', 'N/A')}"])

        lines.append(f"{corner} {c['bold_red']}{url}{c['reset']}\n{div}")
        return "\n".join(lines)

    def _ytdl_opts(self) -> dict:
        """Get yt-dlp options for YouTube extraction."""
        return {
            "quiet": True,
            "extract_flat": True,
            "cachedir": False,
            "extractor_args": {
                "youtube": {
                    "player_client": ["web"],
                    "player_skip": ["configs", "js", "webpage", "authcheck"],
                }
            },
        }

    def search_yt_video(self) -> Generator[str, None, None]:
        """Search YouTube for videos or playlists."""
        try:
            from yt_dlp import YoutubeDL

            search_type = "video" if self._is_track else "playlist"
            with YoutubeDL(self._ytdl_opts()) as ydl:
                info = ydl.extract_info(
                    f"ytsearch{self.limit}:{search_type}:{self.query}", download=False
                )
                entries = info.get("entries", [])

            if not entries:
                yield error(f"No videos matching '{self.query}'\n")
                return

            if self.raw:
                for v in entries:
                    yield str(entries)
                return

            for num, v in enumerate(entries, 1):
                if v_id := v.get("id"):
                    yield self._format_result(
                        num,
                        title=v.get("title", "N/A"),
                        artist=v.get("channel", "N/A"),
                        url=f"https://youtu.be/{v_id}",
                        views=self._fmt_views(v.get("view_count")),
                        duration=self._fmt_duration(v.get("duration")),
                    )

        except KeyboardInterrupt:
            return
        except Exception as e:
            yield styled(f"\nYoutube-Video error: {e}\n", BOLD_RED)

    def search_yt_music(self) -> Generator[str, None, None]:
        """Search YouTube Music for tracks or albums."""
        try:
            from ytmusicapi import YTMusic

            search_type = "songs" if self._is_track else "albums"
            tracks = YTMusic().search(
                query=self.query, limit=self.limit, filter=search_type
            )

            if not tracks:
                yield error(
                    f"No {'tracks' if self._is_track else 'albums'} found for '{self.query}'\n"
                )
                return

            from itertools import islice

            if self.raw:
                for t in islice(tracks, self.limit):
                    yield str(t)
                return

            for num, t in enumerate(islice(tracks, self.limit), 1):
                if self._is_track and (t_id := t.get("videoId")):
                    yield self._format_result(
                        num,
                        title=t.get("title", "Unknown Track"),
                        artist=self._extract_artist(t),
                        album=t.get("album", {}).get("name", "Unknown Album"),
                        url=f"https://music.youtube.com/watch?v={t_id}",
                        views=self._fmt_views(t.get("views")),
                        duration=self._fmt_duration(t.get("duration")),
                    )
                elif pl_id := t.get("playlistId"):
                    yield self._format_result(
                        num,
                        title=t.get("title", "Unknown Album"),
                        artist=self._extract_artist(t),
                        url=f"https://music.youtube.com/playlist?list={pl_id}",
                        year=t.get("year", "N/A"),
                    )

        except KeyboardInterrupt:
            return
        except Exception as e:
            yield styled(f"\nYoutube-Music error: {e}\n", BOLD_RED)

    def search(self) -> Generator[str, None, None]:
        """Execute search based on initialized parameters."""
        yield from self.search_yt_video() if self.yt_video else self.search_yt_music()
