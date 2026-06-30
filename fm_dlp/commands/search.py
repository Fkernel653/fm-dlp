"""YouTube search handlers."""

from typing import Generator

from fm_dlp.utils.colors import (
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
        color: bool,
    ):
        """Initialize search with query parameters.

        Args:
            query: Search query string.
            limit: Maximum number of results.
            yt_video: Search YouTube videos instead of YouTube Music.
            album: Search for albums instead of tracks.
            raw: Output raw Python dicts instead of formatted strings.
            only_url: Output only URLs without formatting.
            color: Colored output.
        """
        self.query = query
        self.limit = limit
        self.yt_video = yt_video
        self.raw = raw
        self.only_url = only_url
        self.type = "album" if album else "track"
        self._is_track = self.type == "track"

        set_colors(color)

        self._c = {
            "bold_cyan": BOLD_CYAN if color else "",
            "bold_red": BOLD_RED if color else "",
            "bold_white": "\033[37m" if color else "",
            "gray": GRAY if color else "",
            "white": "\033[0;37m" if color else "",
            "reset": RESET if color else "",
        }

    @staticmethod
    def _fmt_views(v: str | int | None) -> str:
        """Format view count with commas."""
        if v is None:
            return "N/A"

        if isinstance(v, str):
            return v

        return f"{int(float(v)):,}"

    @staticmethod
    def _fmt_duration(d: str | float | None) -> str:
        """Format duration from seconds to MM:SS or HH:MM:SS."""
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
    def _extract_artist(item: dict) -> str:
        """Extract artist name from YouTube Music response."""
        artists = item.get("artists", [])
        return artists[0].get("name", "Unknown Artist") if artists else "Unknown Artist"

    def _format_result(
        self,
        num: int,
        title: str,
        artist: str,
        url: str,
        **kwargs,
    ) -> str:
        """Format a single search result with optional metadata."""
        c = self._c
        w = c["white"]
        g = c["gray"]

        tree = f"    {g}├─"
        corner = f"    {g}└─"
        sep = f" {g}│{w} "
        div = f"       {g}{'─' * 50}{c['reset']}\n"

        lines = [f"\n{c['bold_cyan']}{num}. {c['bold_white']}{title}"]

        if self.yt_video:
            views = kwargs["views"]
            duration = kwargs["duration"]

            lines.append(f"{tree} {w + artist}")
            lines.append(f"{tree} {w + views}{sep}{w + duration}")

        elif self._is_track:
            album = kwargs["album"]
            views = kwargs["views"]
            duration = kwargs["duration"]

            lines.extend(
                [
                    f"{tree} {w + artist}",
                    f"{tree} {w + album}",
                    f"{tree} {w + views}{sep}{w + duration}",
                ]
            )

        else:
            year = kwargs.get("year", "N/A")
            lines.extend([f"{tree} {w + artist}", f"{tree} {w + year}"])

        lines.append(f"{corner} {c['bold_red']}{url}")
        lines.append(div)

        return "\n".join(lines)

    def _ytdl_opts(self) -> dict:
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
                    yield str(entries) + "\n"
                return

            for num, v in enumerate(entries, 1):
                if v_id := v.get("id"):
                    url = "https://youtu.be/" + v_id

                    if self.only_url:
                        yield url
                    else:
                        yield self._format_result(
                            num,
                            title=v.get("title", "Unknown Video"),
                            artist=v.get("channel", "Unknown Channel"),
                            url=url,
                            views=self._fmt_views(v["view_count"]),
                            duration=self._fmt_duration(v["duration"]),
                        )

        except KeyboardInterrupt:
            return
        except Exception as e:
            yield styled(f"\nYoutube-Video ERROR: {e}\n", BOLD_RED)

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
                    yield str(t) + "\n"
                return

            for num, t in enumerate(islice(tracks, self.limit), 1):
                if self._is_track and (t_id := t.get("videoId")):
                    url = "https://music.youtube.com/watch?v=" + t_id

                    if self.only_url:
                        yield url
                    else:
                        yield self._format_result(
                            num,
                            title=t.get("title", "Unknown Track"),
                            artist=self._extract_artist(t),
                            album=t.get("album", {}).get("name", "Unknown Album"),
                            url=url,
                            views=self._fmt_views(t["views"]),
                            duration=self._fmt_duration(t["duration"]),
                        )
                elif pl_id := t.get("playlistId"):
                    url = "https://music.youtube.com/playlist?list=" + pl_id

                    if self.only_url:
                        yield url
                    else:
                        yield self._format_result(
                            num,
                            title=t.get("title", "Unknown Album"),
                            artist=self._extract_artist(t),
                            year=t.get("year", "N/A"),
                            url=url,
                        )

        except KeyboardInterrupt:
            return
        except Exception as e:
            yield styled(f"\nYoutube-Music ERROR: {e}\n", BOLD_RED)


def search(
    query: str,
    limit: int,
    yt_video: bool,
    album: bool,
    raw: bool,
    only_url: bool,
    color: bool,
):
    """Search YouTube or YouTube Music."""
    s = Search(query, limit, yt_video, album, raw, only_url, color)

    method = "search_yt_video" if yt_video else "search_yt_music"
    return getattr(s, method)()
