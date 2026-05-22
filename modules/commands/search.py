"""
YouTube search handlers.
"""

from dataclasses import dataclass
from itertools import islice
from typing import Any, Generator, cast

from color_kiss import BOLD, CYAN, GRAY, GREEN, RED, RESET


@dataclass
class Search:
    """Handles searching across YouTube and YouTube Music."""

    query: str
    limit: int
    type: str
    proxy: str | None = None

    @staticmethod
    def _fmt_views(v) -> str:
        """Format view count with thousands separator."""
        return f"{int(v):,}" if v else "N/A"

    @staticmethod
    def _fmt_duration(d) -> str:
        """Convert seconds to HH:MM:SS or MM:SS string."""
        if not d:
            return "N/A"
        s = int(d)
        h, remainder = divmod(s, 3600)
        m, s = divmod(remainder, 60)
        return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

    @staticmethod
    def _extract_artist(item: dict) -> str:
        """Extract artist name from ytmusicapi track dict."""
        artists = item.get("artists")
        if artists and artists[0]:
            return artists[0].get("name", "Unknown Artist")
        return "Unknown Artist"

    def _format_result(
        self, num: int, title: str, artist: str, url: str, **kwargs
    ) -> str:
        """Build formatted output string for a single search result."""

        tree = f"    {GRAY}├─{RESET}"
        corner = f"    {GRAY}└─{RESET}"
        sep = f" {GRAY}│{RESET} "
        div = f"       {GRAY}{'─' * 50}{RESET}\n"

        lines = [
            f"\n{BOLD}{CYAN}{num}. {RESET}{BOLD}{title}{RESET}",
            f"{tree} {artist}",
        ]

        if self.type == "track":
            views = kwargs.get("views", "N/A")
            duration = kwargs.get("duration", "N/A")
            lines.append(f"{tree} {views}{sep}{duration}")
        else:
            lines.append(f"{tree} {kwargs.get('year', 'N/A')}")

        lines.append(f"{corner} {RED}{url}{RESET}\n{div}")

        return "\n".join(lines)

    def _ytdl_opts(self) -> dict[str, Any]:
        """Return base yt-dlp options for video search."""
        opts: dict[str, Any] = {
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
        return opts

    def yt_video(self) -> Generator[str, None, None]:
        """Search YouTube videos using yt-dlp."""
        try:
            from yt_dlp import YoutubeDL

            search_type = "playlist" if self.type == "album" else "video"
            opts: Any = self._ytdl_opts()
            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(
                    f"ytsearch{self.limit}:{search_type}:{self.query}", download=False
                )
                videos = info.get("entries") or []

            if not videos:
                yield f"{RED}\nNo videos matching {RESET}'{self.query}'"
                return

            results = []
            videos_list: Any = videos
            for v in islice(videos_list, self.limit):
                v = cast(dict, v)
                if vid_id := v.get("id"):
                    results.append(
                        (
                            v.get("title", "N/A"),
                            v.get("channel", "N/A"),
                            f"https://youtu.be/{vid_id}",
                            self._fmt_views(v.get("view_count")),
                            self._fmt_duration(v.get("duration")),
                        )
                    )

            for num, (title, channel, url, views, duration) in enumerate(results, 1):
                yield self._format_result(
                    num,
                    title=title,
                    artist=channel,
                    url=url,
                    views=views,
                    duration=duration,
                )

        except KeyboardInterrupt:
            yield f"{GREEN}Goodbye!{RESET}"
        except Exception as e:
            yield f"{RED}Youtube-Video error: {e}{RESET}"

    def yt_music(self) -> Generator[str, None, None]:
        """Search YouTube Music for tracks or albums."""
        try:
            from ytmusicapi import YTMusic

            search_type = "albums" if self.type == "album" else "songs"

            yt = YTMusic(
                proxies={"http": self.proxy, "https": self.proxy}
                if self.proxy
                else None
            )
            tracks = yt.search(query=self.query, limit=self.limit, filter=search_type)

            if not tracks:
                yield f"{RED}\nNo tracks found for '{self.query}' on YouTube Music\n{RESET}"
                return

            results = []
            for t in islice(tracks, self.limit):
                t = cast(dict, t)
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
