"""
YouTube search module using the scrapetube library.

This module handles searching for videos on YouTube without requiring an API key.
It includes filtering to ensure results match the original query in title or channel name,
and formats the results for display in the terminal with color-coding.
"""

from modules.colors import RESET, BOLD, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN
import scrapetube


def searching(query: str, limit: int):
    """
    Search YouTube for videos matching the given query and yield formatted results.

    This function uses scrapetube to fetch video results, then filters them to only
    include videos where the query appears in either the title or channel name.
    Each matching video is formatted with color-coded information for terminal display.

    Args:
        query (str): The search term to look for on YouTube.
        limit (int): Maximum number of raw results to fetch before filtering.

    Yields:
        str: Formatted string containing video information (title, channel, date,
             views, duration, and URL) with ANSI color codes for terminal display.
             If no results match after filtering, yields an error message.

    Note:
        The actual number of results may be less than the limit due to filtering.
        The function handles keyboard interrupts and various connection errors gracefully.

    Raises:
        SystemExit: Exits with code 1 if no videos match the query after filtering.
    """
    try:
        # Fetch raw search results from YouTube using scrapetube
        videos = scrapetube.get_search(
            query, limit, sort_by="relevance", results_type="video"
        )

        filtered_results = []
        
        # Filter videos to ensure query appears in title OR channel name
        for video in videos:
            # Extract title text safely, defaulting to "N/A" if missing or malformed
            title = (
                video["title"]["runs"][0]["text"] 
                if "runs" in video.get("title", {}) 
                else "N/A"
            ).lower()
            
            # Extract channel name safely
            channel = (
                video["ownerText"]["runs"][0]["text"] 
                if "ownerText" in video 
                else "N/A"
            ).lower()
            
            query_lower = query.lower()

            # Keep video if query matches title OR channel name
            if query_lower in title or query_lower in channel:
                filtered_results.append(video)

        # Handle case where no videos pass the filter
        if not filtered_results:
            yield f"{RED}\nNo videos matching '{query}' after filtering\n{RESET}"
            return exit(1)

        # Format and yield each filtered video's information
        for num, video in enumerate(filtered_results, start=1):
            # Safely extract all video metadata with fallback values
            video_id = video.get("videoId", "N/A")
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

            # Build formatted output with color-coded labels and values
            video_info = f"""
{BOLD}{num}. {CYAN}Title: {RESET}'{title}'
{MAGENTA}Channel: {RESET}'{channel}'
{BLUE}Creation Date: {RESET}'{date}'
{GREEN}Views: {RESET}'{views}'
{YELLOW}Duration: {RESET}'{duration}'
{RED}URL: {RESET}{BOLD}https://www.youtube.com/watch?v={video_id}{RESET}
"""

            yield video_info

    except KeyboardInterrupt:
        # Graceful exit when user presses Ctrl+C during search
        yield f"{GREEN}Goodbye!{RESET}"

    except (ConnectionAbortedError, ConnectionError, ConnectionRefusedError, ConnectionResetError) as e:
        # Handle various network-related connection errors uniformly
        yield f"{RED}Error: {RESET}{e}"
        return exit(1)