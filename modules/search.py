"""
YouTube search handlers.
"""

from modules.colors import RESET, BOLD, RED, GREEN, CYAN, GRAY
from dataclasses import dataclass
from typing import Generator, Literal
from itertools import islice

from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic


SEPARATE = f"{GRAY}|{RESET}"
DIVIDER = f"   {GRAY}   {'─' * 50}{RESET}\n"


@dataclass
class Search:
    """Handles searching across YouTube"""

    query: str
    limit: int
    type: Literal["track", "album"]
    proxy: str

    def __post_init__(self):
        if self.limit <= 0:
            raise ValueError("Limit must be positive")
        if self.type not in ("track", "album"):
            raise ValueError(f"Invalid type: {self.type}")

    @staticmethod
    def _format_views(v) -> str:
        return f"{int(v):,}" if v else "N/A"

    @staticmethod
    def _format_duration(d) -> str:
        if not d:
            return "N/A"
        s = int(d)
        h, remainder = divmod(s, 3600)
        m, s = divmod(remainder, 60)
        return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

    @staticmethod
    def _extract_artist(item) -> str:
        artists = item.get("artists")
        if artists and artists[0]:
            return artists[0].get("name", "Unknown Artist")
        return "Unknown Artist"

    def _format_result(self, num, title, artist, url, **kwargs) -> str:
        lines = [
            f"\n\n{BOLD}{CYAN}{num}. {RESET}{BOLD}{title}{RESET}",
            f"   {GRAY}├─ {RESET}{artist}",
        ]
        if self.type == "track":
            lines.append(
                f"   {GRAY}├─ {RESET}{kwargs.get('views', 'N/A')} {SEPARATE} {kwargs.get('duration', 'N/A')}"
            )
        else:
            lines.append(f"   {GRAY}├─ {RESET}{kwargs.get('year', 'N/A')}")
        lines.append(f"   {GRAY}└─ {RESET}{RED}{url}{RESET}\n{DIVIDER}")
        return "\n".join(lines)

    def yt_video(self) -> Generator[str, None, None]:
        """Search YouTube videos using yt-dlp."""
        try:
            search_type = "playlist" if self.type == "album" else "video"
            opts = {
                "proxy": self.proxy or None,
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
            with YoutubeDL(opts) as ydl:
                videos = ydl.extract_info(
                    f"ytsearch{self.limit}:{search_type}:{self.query}", download=False
                )["entries"]

            if not videos:
                yield f"{RED}\nNo videos matching {RESET}'{self.query}'"
                return

            results = []
            for v in videos[: self.limit]:
                if vid_id := v.get("id"):
                    results.append(
                        (
                            v.get("title", "N/A"),
                            v.get("channel", "N/A"),
                            f"https://youtu.be/{vid_id}",
                            self._format_views(v.get("view_count")),
                            self._format_duration(v.get("duration")),
                        )
                    )

            for num, (title, channel, url, views, duration) in enumerate(results, 1):
                yield self._format_result(
                    num,
                    title=title,
                    artist=channel,
                    views=views,
                    duration=duration,
                    url=url,
                )

        except KeyboardInterrupt:
            yield f"{GREEN}Goodbye!{RESET}"
        except Exception as e:
            yield f"{RED}Youtube-Video error: {e}{RESET}"

    def yt_music(self) -> Generator[str, None, None]:
        """Search YouTube Music for song tracks only."""
        try:
            search_type = "albums" if self.type == "album" else "songs"
            kwargs = (
                {"proxies": {"http": self.proxy, "https": self.proxy}}
                if self.proxy
                else {}
            )
            yt = YTMusic(**kwargs)
            tracks = yt.search(query=self.query, limit=self.limit, filter=search_type)

            if not tracks:
                yield f"{RED}\nNo tracks found for '{self.query}' on YouTube Music\n{RESET}"
                return

            results = []
            for t in islice(tracks, self.limit):
                if self.type == "track":
                    if vid_id := t.get("videoId"):
                        results.append(
                            (
                                t.get("title", "Unknown Track"),
                                self._extract_artist(t),
                                f"https://music.youtube.com/watch?v={vid_id}",
                                t.get("views", "N/A"),
                                t.get("duration", "N/A"),
                                None,
                            )
                        )
                else:
                    if pl_id := t.get("playlistId"):
                        results.append(
                            (
                                t.get("title", "Unknown Track"),
                                self._extract_artist(t),
                                f"https://music.youtube.com/playlist?list={pl_id}",
                                None,
                                None,
                                t.get("year", "N/A"),
                            )
                        )

            for num, (title, artist, url, views, duration, year) in enumerate(
                results, 1
            ):
                kwargs = (
                    {"views": views, "duration": duration}
                    if self.type == "track"
                    else {"year": year}
                )
                yield self._format_result(num, title, artist, url, **kwargs)

        except KeyboardInterrupt:
            yield f"{GREEN}Goodbye!{RESET}"
        except Exception as e:
            yield f"{RED}Youtube-Music error: {e}{RESET}"
