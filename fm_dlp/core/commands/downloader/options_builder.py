from pathlib import Path
from typing import Any

from ...utils import (
    AUDIO_CODECS,
    VIDEO_CONTAINER_AUDIO_MAP,
    VIDEO_CONTAINERS,
)
from .config import DownloadConfig
from .params import DownloadParams


class OptionsBuilder:
    """Build yt-dlp options dictionary from DownloadParams."""

    def __init__(
        self,
        params: DownloadParams,
        config: DownloadConfig,
    ):
        self.params = params
        self.config = config

        self.conf = self.config.apply_config()

        self.codec = self.conf["codec"]

    def _parse_quality(self) -> str:
        q = self.conf["quality"]

        if q == "best":
            return "bestvideo"
        elif q == "worst":
            return "worstvideo"
        elif q.isdigit():
            return f"bestvideo[height<={q}]"
        elif q.endswith("p") and q[:-1].isdigit():
            return f"bestvideo[height<={q[:-1]}]"

        return q

    def build(self) -> dict[str, Any]:
        """
        Build a complete yt-dlp options dictionary for the download.

        Reads all settings from the resolved config (DownloadConfig), so
        defaults, config-file overrides, and CLI values are already merged
        before this method is called.
        """
        from ...utils.config.params import ConfigParams
        from ...utils.config.path import PathManager

        config_params = ConfigParams(True, self.params.color, self.params.config_file)
        path = Path(PathManager(params=config_params).get_path())

        quiet, jobs = self.conf["quiet"], self.conf["jobs"]

        base_opts: dict[str, Any] = {
            "quiet": quiet,
            "no_warnings": quiet,
            "outtmpl": str(path / "%(title)s.%(ext)s"),
            "concurrent_downloads": jobs,
            "concurrent_fragment_downloads": jobs,
            "extractor_retries": 3,
            "postprocessors": [],
            "keepvideo": self.conf["keep"],
        }

        if self.conf["ffmpeg_path"]:
            base_opts["ffmpeg_location"] = self.conf["ffmpeg_path"]

        if self.conf["remote"]:
            remote = "ejs:npm" if self.conf["remote"] == "npm" else "ejs:github"
            base_opts["remote"] = [remote]

        if not self.params.color:
            base_opts["color"] = "never"

        self._add_cookies(base_opts)

        if self.conf["only_video"]:
            self._build_video_opts(base_opts)
        else:
            self._build_audio_opts(base_opts)

        self._add_subtitles(base_opts)
        self._merge_user_args(base_opts)

        return base_opts

    def _add_cookies(self, opts: dict[str, Any]) -> None:
        cookies = self.conf["cookies"]
        if not cookies:
            return

        cookie_path = Path(cookies)
        if cookie_path.is_file():
            opts["cookiefile"] = str(cookie_path)
        else:
            opts["cookiesfrombrowser"] = (cookies,)

    def _add_subtitles(self, opts: dict[str, Any]) -> None:
        if not self.conf["subtitles"]:
            return
        opts["writesubtitles"] = True
        opts["subtitleslangs"] = [
            s.strip() for s in self.conf["subtitle_langs"].split(",") if s.strip()
        ]
        opts["writeautomaticsub"] = self.conf["auto_subs"]

        if self.conf["embed_subs"]:
            codec_is_video = self.codec in VIDEO_CONTAINERS or self.conf["only_video"]
            if not codec_is_video:
                return

            opts["embedsubtitles"] = True
            opts.setdefault("postprocessors", []).append({"key": "FFmpegEmbedSubtitle"})

    def _merge_user_args(self, opts: dict[str, Any]) -> None:
        user_args = self.conf["ytdlp_args"]
        if not user_args:
            return

        for key, value in user_args.items():
            if key == "postprocessors":
                existing = opts.get("postprocessors", [])
                if isinstance(value, list):
                    existing.extend(value)
                else:
                    existing.append(value)
                opts["postprocessors"] = existing
            else:
                opts[key] = value

    def _build_video_opts(self, opts: dict[str, Any]) -> None:
        opts["format"] = self._parse_quality()

        if self.codec in VIDEO_CONTAINERS:
            opts["postprocessors"].append(
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": self.codec,
                }
            )

    def _build_audio_opts(self, opts: dict[str, Any]) -> None:
        if self.codec in AUDIO_CODECS:
            self._build_audio_only_opts(opts)
        elif self.codec in VIDEO_CONTAINERS:
            self._build_video_with_audio_opts(opts)

    def _build_audio_only_opts(self, opts: dict[str, Any]) -> None:
        opts["format"] = "bestaudio/best"
        opts["postprocessors"].append(
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": self.codec,
                "preferredquality": str(self.conf["kbps"]),
            }
        )

        if self.conf["metadata"]:
            opts["postprocessors"].extend(
                [
                    {"key": "FFmpegMetadata"},
                    {"key": "EmbedThumbnail"},
                ]
            )
            opts["embedmetadata"] = True
            opts["writethumbnail"] = True

    def _build_video_with_audio_opts(self, opts: dict[str, Any]) -> None:
        audio_ext = VIDEO_CONTAINER_AUDIO_MAP[self.codec]

        opts["format"] = f"{self._parse_quality()}+bestaudio[ext={audio_ext}]/best"

        opts["postprocessors"].append(
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": self.codec,
            }
        )
