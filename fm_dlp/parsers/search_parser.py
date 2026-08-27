def create_search_parser(subparsers) -> None:
    """Create and configure the search command parser.

    Args:
        subparsers: Subparsers object from argparse.ArgumentParser.
    """

    search_parser = subparsers.add_parser(
        "search",
        help="Search for music tracks or videos on YouTube/YTMusic",
        description="Search for music tracks or videos on YouTube/YTMusic",
    )
    search_parser.add_argument("query", help="Search query string")
    search_parser.add_argument(
        "-l",
        "--limit",
        type=int,
        choices=range(1, 101),
        default=10,
        metavar="1-100",
        help="Maximum number of results to return (default: 10)",
    )
    search_parser.add_argument(
        "-v",
        "--yt-video",
        action="store_true",
        help="Search for YouTube videos instead of music tracks",
    )
    search_parser.add_argument(
        "-a",
        "--album",
        action="store_true",
        help="Search for albums instead of individual tracks",
    )
    search_parser.add_argument(
        "-r",
        "--raw",
        action="store_true",
        help="Output results in raw format (Python dict representation)",
    )
    search_parser.add_argument(
        "-u",
        "--only-url",
        action="store_true",
        help="Output only the URLs without any formatting",
    )
