"""
YouTube and SoundCloud search module.

Provides asynchronous search functionality for both YouTube (using scrapetube)
and SoundCloud platforms. Displays results with thumbnails, metadata, and URLs.
"""

from modules.colors import RESET, BOLD, RED, GREEN, CYAN, GRAY
from fake_useragent import UserAgent
import asyncio
import traceback


class Search:
    """Handles searching across multiple music platforms (YouTube and SoundCloud)."""

    def __init__(self, query: str, limit: int, enable_filter: str):
        """
        Initialize search with query parameters.

        Args:
            query: Search term to look for
            limit: Maximum number of results to return
            enable_filter: String 'true'/'false' to filter out invalid results
        """
        self.query = query
        self.limit = limit
        self.enable_filter = enable_filter

        self.ua = UserAgent().random
        self.sep = f"{GRAY}|{RESET}"  # Separator for metadata display

    def view_image(self, url: str, max_height: int = 10) -> str:
        """
        Fetch and format thumbnail image for terminal display.

        Args:
            url: Image URL to display
            max_height: Maximum height in rows for the terminal image

        Returns:
            String representation of the image for terminal rendering,
            or error message if term_image is not available
        """
        if not url:
            return ""

        try:
            from term_image.image import from_url

            image = from_url(url=url)

            if image is None:
                return ""

            try:
                import shutil

                terminal_width = shutil.get_terminal_size().columns
                width = min(50, terminal_width - 10)
                image.width = width

                if image.height > max_height * 4:
                    image.height = max_height * 4
            except (AttributeError, ValueError, TypeError, OSError):
                image.height = max_height * 4

            return str(image)

        except ImportError:
            return (
                f"{GRAY}[Image preview not available: term_image not installed]{RESET}"
            )
        except Exception as e:
            return f"{GRAY}[Image: {str(e)[:50]}]{RESET}"

    async def youtube(self):
        """
        Search YouTube for videos matching the query using scrapetube.

        Yields:
            Formatted strings containing video information including:
            - Thumbnail image (if term_image available)
            - Result number and title
            - Channel name
            - Publication date, view count, and duration
            - YouTube URL

        Exits with error codes for various failure scenarios including timeouts,
        network errors, missing modules, and YouTube API structure changes.
        """
        import scrapetube

        def sync_search():
            """Synchronous search wrapper for execution in thread pool."""
            try:
                videos = scrapetube.get_search(
                    query=self.query,
                    limit=self.limit,
                    sort_by="relevance",
                    results_type="video",
                )
                if self.enable_filter == "true":
                    filtered_videos = []
                    for video in videos:
                        if video.get("videoId") and video.get("title"):
                            filtered_videos.append(video)
                            if len(filtered_videos) >= self.limit:
                                break

                    return filtered_videos
                else:
                    return list(videos)

            except scrapetube.ScrapeError as e:
                raise Exception(f"Scrapetube scraping error: {e}")
            except ValueError as e:
                raise Exception(f"Invalid parameter in search: {e}")
            except Exception as e:
                raise Exception(f"Unexpected error in sync_search: {e}")

        try:
            loop = asyncio.get_event_loop()

            videos = await asyncio.wait_for(
                loop.run_in_executor(None, sync_search), timeout=10.0
            )

            if not videos:
                yield f"{RED}\nNo videos matching {RESET}'{self.query}'"
                return

            # Format and yield each filtered video's information
            for num, video in enumerate(videos, 1):
                video_id = video.get("videoId", "N/A")

                thumbnails = video.get("thumbnail", {}).get("thumbnails", [])
                image_url = thumbnails[0]["url"] if thumbnails else None

                title = (
                    video["title"]["runs"][0]["text"]
                    if "runs" in video.get("title", {})
                    else "N/A"
                )
                channel = (
                    video["ownerText"]["runs"][0]["text"]
                    if "ownerText" in video
                    else "N/A"
                )
                date = (
                    video["publishedTimeText"]["simpleText"]
                    if "publishedTimeText" in video
                    else "N/A"
                )
                views = (
                    video["viewCountText"]["simpleText"]
                    if "viewCountText" in video
                    else "N/A"
                )
                duration = (
                    video["lengthText"]["accessibility"]["accessibilityData"]["label"]
                    if "lengthText" in video
                    else "N/A"
                )

                video_info = (
                    f"\n\n{self.view_image(url=image_url)}\n"
                    f"\n{BOLD}{CYAN}{num}. {RESET}{BOLD}{title}{RESET}\n"
                    f"   {GRAY}├─ {RESET}{channel}\n"
                    f"   {GRAY}├─ {RESET}{date} {self.sep} {views} {self.sep} {duration}\n"
                    f"   {GRAY}└─ {RESET}{RED}https://youtu.be/{video_id}{RESET}\n"
                    f"   {GRAY}   {'─' * 50}{RESET}\n"
                )
                yield video_info

        except asyncio.TimeoutError:
            print(f"\n{RED}The search took more than 10 seconds.{RESET}")
            print(
                f"{RED}Try reducing your search limit or check your connection{RESET}\n"
            )
            exit(1)

        except ConnectionError as e:
            print(f"{RED}Network connection error: {RESET}{e}")
            print(f"{RED}Please check your internet connection{RESET}\n")
            exit(1)

        except ImportError as e:
            print(f"{RED}Missing module error: {RESET}{e}")
            print(
                f"{RED}Try reinstalling dependencies: pip install -r requirements.txt{RESET}\n"
            )
            exit(1)

        except AttributeError as e:
            print(f"{RED}Data structure error: {RESET}{e}")
            print(f"{RED}YouTube API may have changed. Update scrapetube.{RESET}\n")
            exit(1)

        except KeyError as e:
            print(f"{RED}Missing key in response: {RESET}{e}")
            print(f"{RED}YouTube response structure changed.{RESET}\n")
            exit(1)

        except Exception as e:
            print(f"{RED}Unexpected error in YouTube search:{RESET}")
            print(f"{RED}Type: {type(e).__name__}{RESET}")
            print(f"{RED}Message: {e}{RESET}")
            print(f"{GRAY}Traceback:{RESET}")
            traceback.print_exc()
            print(f"\n{RED}Please report this issue with the traceback above{RESET}\n")
            exit(1)

        except KeyboardInterrupt:
            print(f"{GREEN}Goodbye!{RESET}")
            exit(0)

    async def soundcloud(self):
        """
        Search SoundCloud for tracks matching the query.

        Yields:
            Formatted strings containing track information including:
            - Artwork thumbnail (if term_image available)
            - Result number and title
            - Artist/channel name
            - Publication date and duration
            - Track URL

        Exits with error codes for timeouts, network errors, missing modules,
        and API structure changes.
        """
        from soundcloud import SoundCloud
        from itertools import islice

        try:
            loop = asyncio.get_event_loop()

            def sync_search():
                """Synchronous SoundCloud search wrapper."""
                try:
                    sc = SoundCloud(user_agent=self.ua)
                    tracks = sc.search_tracks(self.query)
                    return list(islice(tracks, self.limit))

                    if self.enable_filter == "true":
                        filtered_tracks = []
                        for track in tracks:
                            if (
                                hasattr(track, "id")
                                and track.id
                                and hasattr(track, "title")
                                and track.title
                            ):
                                filtered_tracks.append(track)
                                if len(filtered_tracks) >= self.limit:
                                    break

                                return list(islice(filtered_tracks, self.limit))
                    else:
                        return list(islice(tracks, self.limit))

                except AttributeError as e:
                    raise Exception(f"SoundCloud object missing attribute: {e}")
                except TypeError as e:
                    raise Exception(f"Invalid parameter type in search: {e}")
                except Exception as e:
                    raise Exception(f"SoundCloud search failed: {e}")

            tracks = await asyncio.wait_for(
                loop.run_in_executor(None, sync_search), timeout=30.0
            )

            if not tracks:
                yield f"{RED}\nNo tracks found for '{self.query}' on SoundCloud\n{RESET}"
                return

            for num, track in enumerate(tracks, 1):
                try:
                    image_url = track.artwork_url
                    channel = track.user.full_name
                    date = track.created_at.date()

                    duration_ms = getattr(track, "duration", 0)
                    minutes = duration_ms // 60000
                    seconds = (duration_ms % 60000) // 1000
                    duration_str = f"{minutes}:{seconds:02d}"

                    track_url = getattr(track, "permalink_url", None) or getattr(
                        track, "uri", "URL not available"
                    )

                    track_info = (
                        f"\n\n{self.view_image(url=image_url)}\n"
                        f"\n{BOLD}{CYAN}{num}. {RESET}{BOLD}{track.title}{RESET}\n"
                        f"   {GRAY}├─ {RESET}{channel}\n"
                        f"   {GRAY}├─ {RESET}{date} {self.sep} {duration_str}\n"
                        f"   {GRAY}└─ {RESET}{RED}{track_url}{RESET}\n"
                        f"   {GRAY}   {'─' * 50}{RESET}\n"
                    )
                    yield track_info
                except AttributeError as e:
                    yield f"{RED}\n[Error formatting track #{num}: missing attribute - {e}]{RESET}\n"
                except Exception as e:
                    yield f"{RED}\n[Error formatting track #{num}: {type(e).__name__} - {e}]{RESET}\n"

        except asyncio.TimeoutError:
            print(f"{RED}SoundCloud search timeout (30 seconds){RESET}")
            print(f"{RED}Try again later or reduce search limit{RESET}\n")
            exit(1)

        except ConnectionError as e:
            print(f"{RED}Network connection error for SoundCloud: {RESET}{e}")
            print(f"{RED}Please check your internet connection{RESET}\n")
            exit(1)

        except ImportError as e:
            print(f"{RED}SoundCloud module import error: {RESET}{e}")
            print(f"{RED}Install soundcloud package: pip install soundcloud{RESET}\n")
            exit(1)

        except TypeError as e:
            print(f"{RED}Type error in SoundCloud search: {RESET}{e}")
            print(f"{RED}Check query parameter type (should be string){RESET}\n")
            exit(1)

        except Exception as e:
            print(f"{RED}Unexpected error in SoundCloud search:{RESET}")
            print(f"{RED}Type: {type(e).__name__}{RESET}")
            print(f"{RED}Message: {e}{RESET}")
            print(f"{GRAY}Traceback:{RESET}")
            traceback.print_exc()
            print(f"\n{RED}Please report this issue with the traceback above{RESET}\n")
            exit(1)

        except KeyboardInterrupt:
            print(f"{GREEN}Goodbye!{RESET}")
            exit(0)
