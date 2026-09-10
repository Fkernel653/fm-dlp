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
    add_arg = search_parser.add_argument

    add_arg("query", help="Search query string")
    add_arg(
        "-l",
        "--limit",
        type=int,
        choices=range(1, 101),
        default=10,
        metavar="1-100",
        help="Maximum number of results to return (default: 10)",
    )
    add_arg(
        "-v",
        "--yt-video",
        action="store_true",
        help="Search for YouTube videos instead of music tracks",
    )
    add_arg(
        "-a",
        "--album",
        action="store_true",
        help="Search for albums instead of individual tracks",
    )
    add_arg(
        "-r",
        "--raw",
        action="store_true",
        help="Output results in raw format (Python dict representation)",
    )
    add_arg(
        "-u",
        "--only-url",
        action="store_true",
        help="Output only the URLs without any formatting",
    )
