"""YouTube search handlers."""

from typing import Any, Generator

from fm_dlp.utils.colors import (
    BOLD,
    BOLD_CYAN,
    BOLD_RED,
    GRAY,
    RESET,
    error,
    styled,
)


class Search:
    """Handles searching across YouTube and YouTube Music."""

    def __init__(self, query: str, limit: int, type: str):
        self.query = query
        self.limit = limit
        self.type = type
        self._is_track = type == "track"

    @staticmethod
    def _fmt_views(v: Any) -> str:
        if v is None:
            return "N/A"
        try:
            return f"{int(float(v)):,}"
        except (ValueError, TypeError):
            return str(v)

    @staticmethod
    def _fmt_duration(d: Any) -> str:
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
        artists = item["artists"]
        if artists and artists[0]:
            return artists[0].get("name", "Unknown Artist")
        return "Unknown Artist"

    def _format_result(
        self, num: int, title: str, artist: str, url: str, **kwargs: Any
    ) -> str:
        tree = f"    {GRAY}├─{RESET}"
        corner = f"    {GRAY}└─{RESET}"
        sep = f" {GRAY}│{RESET} "
        div = f"       {GRAY}{'─' * 50}{RESET}\n"

        lines = [
            f"\n{BOLD_CYAN}{num}. {RESET}{BOLD}{title}{RESET}",
            f"{tree} {artist}",
        ]

        if self._is_track:
            views = kwargs.get("views", "N/A")
            duration = kwargs.get("duration", "N/A")
            lines.append(f"{tree} {views}{sep}{duration}")
        else:
            lines.append(f"{tree} {kwargs.get('year', 'N/A')}")

        lines.append(f"{corner} {BOLD_RED}{url}{RESET}\n{div}")
        return "\n".join(lines)

    def _ytdl_opts(self) -> dict[str, Any]:  # type: ignore[explicit-any]
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

    def yt_video(self) -> Generator[str, None, None]:
        try:
            from yt_dlp import YoutubeDL

            search_type = "video" if self._is_track else "playlist"
            with YoutubeDL(self._ytdl_opts()) as ydl:  # type: ignore[explicit-any]
                info = ydl.extract_info(
                    f"ytsearch{self.limit}:{search_type}:{self.query}", download=False
                )
                entries = info.get("entries", [])  # type: ignore[assignment]

            if not entries:
                yield error(f"No videos matching '{self.query}'\n")
                return

            for num, v in enumerate(entries, 1):  # type: ignore[arg-type]
                if v_id := v["id"]:
                    url = "https://youtu.be/" + v_id
                    yield self._format_result(
                        num,
                        title=v.get("title", "N/A"),
                        artist=v.get("channel", "N/A"),
                        url=url,
                        views=self._fmt_views(v["view_count"]),
                        duration=self._fmt_duration(v["duration"]),
                    )

        except KeyboardInterrupt:
            return
        except Exception as e:
            yield styled(f"\nYoutube-Video error: {e}\n", BOLD_RED)

    def yt_music(self) -> Generator[str, None, None]:
        try:
            from ytmusicapi import YTMusic

            search_type = "songs" if self._is_track else "albums"
            ytmusic = YTMusic()
            tracks = ytmusic.search(
                query=self.query, limit=self.limit, filter=search_type
            )

            if not tracks:
                yield error(f"No tracks found for '{self.query}' on YouTube Music\n")
                return

            from itertools import islice

            for num, t in enumerate(islice(tracks, self.limit), 1):
                if self._is_track:
                    if t_id := t["videoId"]:
                        url = "https://music.youtube.com/watch?v=" + t_id
                        yield self._format_result(
                            num,
                            title=t.get("title", "Unknown Track"),
                            artist=self._extract_artist(t),
                            url=url,
                            views=self._fmt_views(t.get("views", "N/A")),
                            duration=self._fmt_duration(t.get("duration", "N/A")),
                        )
                elif pl_id := t["playlistId"]:
                    url = "https://music.youtube.com/playlist?list=" + pl_id
                    yield self._format_result(
                        num,
                        title=t.get("title", "Unknown Track"),
                        artist=self._extract_artist(t),
                        url=url,
                        year=t.get("year", "N/A"),
                    )

        except KeyboardInterrupt:
            return
        except Exception as e:
            yield styled(f"\nYoutube-Music error: {e}\n", BOLD_RED)

    def search(self, platform: str) -> Generator[str, None, None]:
        match platform:
            case "yt-video":
                yield from self.yt_video()
            case "yt-music":
                yield from self.yt_music()
