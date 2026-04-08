from mutagen.id3 import ID3, TIT2, TPE1, TALB
from pathlib import Path


def add_metadata(file: Path, codec: str, title: str, artist: str, album: str):
    """Add metadata tags to audio file based on its codec/format."""
    match codec.lower():
        case "m4a":
            # M4A/MP4 format - uses iTunes-style metadata keys
            from mutagen.mp4 import MP4

            audio = MP4(file)
            audio["\xa9nam"] = title   # song title
            audio["\xa9ART"] = artist  # artist name
            audio["\xa9alb"] = album   # album name
            audio.save()
            return True

        case "mp3":
            # MP3 format - uses ID3 tags
            from mutagen.mp3 import MP3

            audio = MP3(file, ID3=ID3)
            if audio.tags is None:
                audio.add_tags()  # create ID3 tags if missing
            audio.tags.add(TIT2(encoding=3, text=title))   # title tag
            audio.tags.add(TPE1(encoding=3, text=artist))  # artist tag
            audio.tags.add(TALB(encoding=3, text=album))   # album tag
            audio.save()
            return True

        case "flac":
            # FLAC format - uses Vorbis comments
            from mutagen.flac import FLAC

            audio = FLAC(file)
            audio["title"] = title
            audio["artist"] = artist
            audio["album"] = album
            audio.save()
            return True

        case "opus":
            # Opus format in Ogg container
            from mutagen.oggopus import OggOpus

            audio = OggOpus(file)
            audio["title"] = title
            audio["artist"] = artist
            audio["album"] = album
            audio.save()
            return True

        case _:
            raise ValueError(f"Unsupported codec: {codec}")