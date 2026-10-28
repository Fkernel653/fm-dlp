from dataclasses import dataclass


@dataclass
class DownloadParams:
    """
    Data container for all download configuration parameters.

    Aggregates all settings required for a download operation: URL, format
    preferences (codec, bitrate, quality), output handling (path, keep, save),
    and authentication (cookies). All fields are required at instantiation
    to ensure explicit configuration.

    Attributes:
        url: Target YouTube/YouTube Music URL.
        codec: Audio format (mp3, m4a, flac, wav, opus, etc.).
        kbps: Audio bitrate in kbps.
        quality: Video quality preset (e.g., '1080p', '720p', 'best').
        jobs: Number of concurrent download workers.
        quiet: Suppress console output if True.
        metadata: Embed tags and thumbnails if True.
        keep: Keep intermediate files after download if True.
        save: Persist configuration for future use if True.
        use_config: Load settings from config file if True.
        path: Output directory path.
        ffmpeg_path: The way binary file FFmpeg
        config_file: Custom path to the TOML config file. If None, the platform-specific default is used.
        only_video: Download video only (skip audio extraction) if True.
        cookies: Path to Netscape-format cookies file (optional).
        remote: Remote destination path for uploads (optional).
        color: Enable colored console output if True.
        subtitles: Download subtitles if True.
        subtitle_langs: Comma-separated subtitle language codes (e.g. 'en,ru').
        embed_subs: Embed subtitles into the video container if True.
        auto_subs: Include auto-generated subtitles if True.
        ytdlp_args: Additional raw yt-dlp CLI-style arguments (optional).
    """

    url: str
    codec: str
    kbps: int
    quality: str
    jobs: int
    quiet: bool
    metadata: bool
    keep: bool
    save: bool
    use_config: bool
    path: str | None
    ffmpeg_path: str | None
    config_file: str | None
    only_video: bool
    cookies: str | None
    remote: str | None
    subtitles: bool
    subtitle_langs: str | None
    embed_subs: bool
    auto_subs: bool
    color: bool
    ytdlp_args: dict[str, object] | None
