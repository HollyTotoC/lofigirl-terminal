"""
YouTube stream fetcher for LofiGirl Terminal.

This module handles fetching real streaming URLs from YouTube live streams
using yt-dlp. It extracts the direct stream URL that can be played by mpv.
"""

import subprocess
from dataclasses import dataclass
from typing import Optional

from lofigirl_terminal.logger import get_logger

logger = get_logger(__name__)


@dataclass
class StreamInfo:
    """
    Information about a YouTube stream.

    Attributes:
        url: Direct streaming URL
        title: Stream title
        thumbnail: Thumbnail URL
        description: Stream description
        is_live: Whether the stream is currently live
        format_id: Format ID of the stream
        format_note: Format quality note (e.g., "1080p", "audio only")
    """

    url: str
    title: str
    thumbnail: Optional[str] = None
    description: Optional[str] = None
    is_live: bool = False
    format_id: Optional[str] = None
    format_note: Optional[str] = None


class YouTubeFetcher:
    """
    Fetches YouTube stream information and URLs using yt-dlp.

    This class provides methods to extract streaming URLs from YouTube videos,
    especially for live streams. It uses yt-dlp to get the best quality audio
    stream or video stream URL.
    """

    def __init__(self, prefer_audio_only: bool = True) -> None:
        """
        Initialize the YouTube fetcher.

        Args:
            prefer_audio_only: If True, prefer audio-only streams for better
                             performance. If False, get video streams.
        """
        self.prefer_audio_only = prefer_audio_only
        logger.debug(f"YouTubeFetcher initialized (audio_only={prefer_audio_only})")

    def get_stream_url(self, youtube_url: str) -> Optional[str]:
        """
        Get the direct streaming URL from a YouTube URL.

        This method uses yt-dlp to extract the actual streaming URL that can
        be played by media players like mpv.

        Args:
            youtube_url: The YouTube video/stream URL

        Returns:
            Direct streaming URL if successful, None otherwise

        Example:
            >>> fetcher = YouTubeFetcher()
            >>> url = fetcher.get_stream_url("https://www.youtube.com/watch?v=jfKfPfyJRdk")
            >>> print(url)
            https://...m3u8
        """
        try:
            logger.info(f"Fetching stream URL for: {youtube_url}")

            # Build yt-dlp command
            cmd = [
                "yt-dlp",
                "--get-url",
                "--no-warnings",
            ]

            # Add format selector based on preference
            if self.prefer_audio_only:
                cmd.extend(["-f", "bestaudio/best"])
            else:
                cmd.extend(["-f", "best"])

            cmd.append(youtube_url)

            # Execute yt-dlp
            # Safe: command is built from a list, not shell=True
            result = subprocess.run(  # nosec B603
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

            if result.returncode == 0 and result.stdout:
                stream_url = result.stdout.strip()
                logger.info("Successfully fetched stream URL")
                logger.debug(f"Stream URL: {stream_url[:100]}...")
                return stream_url
            else:
                logger.error(f"Failed to fetch stream URL: {result.stderr}")
                return None

        except subprocess.TimeoutExpired:
            logger.error(f"Timeout while fetching stream URL for {youtube_url}")
            return None
        except Exception as e:
            logger.exception(f"Error fetching stream URL: {e}")
            return None

    def get_stream_info(self, youtube_url: str) -> Optional[StreamInfo]:
        """
        Get detailed information about a YouTube stream.

        This method fetches both the streaming URL and metadata about the stream.

        Args:
            youtube_url: The YouTube video/stream URL

        Returns:
            StreamInfo object if successful, None otherwise

        Example:
            >>> fetcher = YouTubeFetcher()
            >>> info = fetcher.get_stream_info("https://www.youtube.com/watch?v=...")
            >>> print(info.title)
            lofi hip hop radio 📚 - beats to relax/study to
        """
        try:
            logger.info(f"Fetching stream info for: {youtube_url}")

            # Build yt-dlp command to get JSON info
            cmd = [
                "yt-dlp",
                "--dump-json",
                "--no-warnings",
                "--skip-download",
            ]

            # Add format selector
            if self.prefer_audio_only:
                cmd.extend(["-f", "bestaudio/best"])
            else:
                cmd.extend(["-f", "best"])

            cmd.append(youtube_url)

            # Execute yt-dlp
            # Safe: command is built from a list, not shell=True
            result = subprocess.run(  # nosec B603
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

            if result.returncode == 0 and result.stdout:
                import json

                data = json.loads(result.stdout)

                # Extract stream info
                stream_info = StreamInfo(
                    url=data.get("url", ""),
                    title=data.get("title", "Unknown Title"),
                    thumbnail=data.get("thumbnail"),
                    description=data.get("description", ""),
                    is_live=data.get("is_live", False),
                    format_id=data.get("format_id"),
                    format_note=data.get("format_note"),
                )

                logger.info(f"Successfully fetched stream info: {stream_info.title}")
                return stream_info
            else:
                logger.error(f"Failed to fetch stream info: {result.stderr}")
                return None

        except subprocess.TimeoutExpired:
            logger.error(f"Timeout while fetching stream info for {youtube_url}")
            return None
        except Exception as e:
            logger.exception(f"Error fetching stream info: {e}")
            return None

    def check_yt_dlp_installed(self) -> bool:
        """
        Check if yt-dlp is installed and accessible.

        Returns:
            True if yt-dlp is available, False otherwise

        Example:
            >>> fetcher = YouTubeFetcher()
            >>> if fetcher.check_yt_dlp_installed():
            ...     print("yt-dlp is ready!")
        """
        try:
            # Safe: command is built from a list, not shell=True
            result = subprocess.run(  # nosec B603
                ["yt-dlp", "--version"],
                capture_output=True,
                timeout=5,
                check=False,
            )
            is_installed = result.returncode == 0

            if is_installed:
                version = result.stdout.decode().strip()
                logger.info(f"yt-dlp is installed: {version}")
            else:
                logger.warning("yt-dlp is not installed or not accessible")

            return is_installed

        except (FileNotFoundError, subprocess.TimeoutExpired):
            logger.warning("yt-dlp is not installed")
            return False


# Cached fetcher instance
_fetcher: Optional[YouTubeFetcher] = None


def get_fetcher(prefer_audio_only: bool = True) -> YouTubeFetcher:
    """
    Get or create a cached YouTubeFetcher instance.

    Args:
        prefer_audio_only: Whether to prefer audio-only streams

    Returns:
        YouTubeFetcher instance

    Example:
        >>> fetcher = get_fetcher()
        >>> url = fetcher.get_stream_url("https://youtube.com/...")
    """
    global _fetcher
    if _fetcher is None:
        _fetcher = YouTubeFetcher(prefer_audio_only=prefer_audio_only)
    return _fetcher
