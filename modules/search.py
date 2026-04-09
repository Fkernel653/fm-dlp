# search.py
"""
YouTube and SoundCloud search module with async support.
"""

from modules.colors import RESET, BOLD, RED, GREEN, CYAN, GRAY
from dataclasses import dataclass

from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic
from soundcloud import SoundCloud

from fake_useragent import UserAgent
from itertools import islice


@dataclass
class Search:
    """Handles searching across YouTube and SoundCloud."""

    query: str
    limit: int
    sep = f"{GRAY}|{RESET}"

    def yt_video(self):
        """Search YouTube using yt-dlp."""
        try:
            opts = {"quiet": True, "extract_flat": True, "simulate": True}
            with YoutubeDL(opts) as ydl:
                # Extract video entries from search results
                videos = ydl.extract_info(
                    f"ytsearch{self.limit}:{self.query}", download=False
                )["entries"]

            if not videos:
                yield f"{RED}\nNo videos matching {RESET}'{self.query}'"

            for num, video in enumerate(videos, 1):
                # Format view count with commas
                views = video.get("view_count", "N/A")
                if views and isinstance(views, int):
                    views = f"{views:,}"

                # Convert seconds to MM:SS format
                duration_sec = video.get("duration")
                if duration_sec:
                    minutes = int(duration_sec // 60)
                    seconds = int(duration_sec % 60)
                    duration_str = f"{minutes}:{seconds:02d}"
                else:
                    duration_str = "N/A"

                # Build formatted output with tree-like structure
                video_info = (
                    f"\n\n{BOLD}{CYAN}{num}. {RESET}{BOLD}{video.get('title', 'N/A')}{RESET}\n"
                    f"   {GRAY}├─ {RESET}{video.get('channel', 'N/A')}\n"
                    f"   {GRAY}├─ {RESET}{views} {self.sep} {duration_str}\n"
                    f"   {GRAY}└─ {RESET}{RED}https://youtu.be/{video.get('id')}{RESET}\n"
                    f"   {GRAY}   {'─' * 50}{RESET}"
                )
                yield video_info

        except Exception as e:
            yield f"{RED}Youtube-Video error: {e}{RESET}"
        except KeyboardInterrupt:
            yield f"{GREEN}Goodbye!{RESET}"

    def yt_music(self):
        """Search YouTube Music for song tracks only."""
        try:
            yt = YTMusic()
            tracks = yt.search(
                query=self.query, limit=self.limit, filter="songs"
            )  # song filter only

            if not tracks:
                yield f"{RED}\nNo tracks found for '{self.query}' on YouTube Music\n{RESET}"

            for num, track in enumerate(tracks, 1):
                video_id = track.get("videoId", "N/A")

                # Extract first artist from artists list
                artists_list = track.get("artists", [])
                if artists_list and len(artists_list) > 0:
                    artist = artists_list[0].get("name", "Unknown Artist")
                else:
                    artist = "Unknown Artist"

                track_info = (
                    f"\n{BOLD}{CYAN}{num}. {RESET}{BOLD}{track.get('title', 'Unknown Track')}{RESET}\n"
                    f"   {GRAY}├─ {RESET}{artist}\n"
                    f"   {GRAY}├─ {RESET}{track.get('duration', 'N/A')}\n"
                    f"   {GRAY}└─ {RESET}{RED}{f'https://music.youtube.com/watch?v={video_id}'}{RESET}\n"
                    f"   {GRAY}   {'─' * 50}{RESET}\n"
                )
                yield track_info

        except Exception as e:
            yield f"{RED}Youtube-Music error: {e}{RESET}"
        except KeyboardInterrupt:
            yield f"{GREEN}Goodbye!{RESET}"

    def soundcloud(self):
        """Search SoundCloud for tracks."""
        try:
            ua = UserAgent().random
            sc = SoundCloud(user_agent=ua)
            tracks = islice(sc.search_tracks(self.query), self.limit)

            if not tracks:
                yield f"{RED}\nNo tracks found for '{self.query}' on SoundCloud\n{RESET}"

            for num, track in enumerate(tracks, 1):
                title = track.title if track.title else "Unknown Track"
                artist = (
                    track.user.full_name if track.user.full_name else "Unknown Artist"
                )

                date = track.created_at.date() if track.created_at.date() else "N/A"

                # Convert milliseconds to MM:SS format
                duration_ms = getattr(track, "duration", 0)
                minutes = duration_ms // 60000
                seconds = (duration_ms % 60000) // 1000
                duration_str = f"{minutes}:{seconds:02d}"

                # Get track URL from permalink or URI
                track_url = getattr(track, "permalink_url", None) or getattr(
                    track, "uri", "N/A"
                )

                track_info = (
                    f"\n{BOLD}{CYAN}{num}. {RESET}{BOLD}{title}{RESET}\n"
                    f"   {GRAY}├─ {RESET}{artist}\n"
                    f"   {GRAY}├─ {RESET}{date} {self.sep} {duration_str}\n"
                    f"   {GRAY}└─ {RESET}{RED}{track_url}{RESET}\n"
                    f"   {GRAY}   {'─' * 50}{RESET}\n"
                )
                yield track_info

        except Exception as e:
            yield f"{RED}SoundCloud error: {e}{RESET}"
        except KeyboardInterrupt:
            yield f"{GREEN}Goodbye!{RESET}"
