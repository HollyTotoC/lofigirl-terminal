"""
Real audio/video player module using python-mpv for LofiGirl Terminal.

This module provides actual audio and video playback using mpv media player.
It supports YouTube streams via yt-dlp integration and provides full
playback control.
"""

from enum import Enum
from typing import Callable, Optional

try:
    import mpv

    MPV_AVAILABLE = True
except ImportError:
    MPV_AVAILABLE = False

from lofigirl_terminal.config import get_config
from lofigirl_terminal.logger import get_logger
from lofigirl_terminal.modules.stations import Station
from lofigirl_terminal.modules.youtube_fetcher import get_fetcher

logger = get_logger(__name__)


class PlayerState(Enum):
    """
    Enum representing the player state.

    Attributes:
        STOPPED: Player is stopped
        PLAYING: Player is currently playing
        PAUSED: Player is paused
        BUFFERING: Player is buffering content
        LOADING: Player is loading a stream
        ERROR: Player encountered an error
    """

    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"
    BUFFERING = "buffering"
    LOADING = "loading"
    ERROR = "error"


class MPVPlayer:
    """
    Real audio/video player using python-mpv.

    This player can stream YouTube videos/audio using yt-dlp integration
    and provides full control over playback, volume, seeking, etc.

    Attributes:
        state: Current player state
        volume: Current volume level (0-100)
        muted: Whether audio is muted
        current_station: Currently loaded station
        is_video_mode: Whether playing video or audio-only
    """

    def __init__(self, video_mode: bool = False) -> None:
        """
        Initialize the MPV player.

        Args:
            video_mode: If True, display video. If False, audio-only mode.

        Raises:
            RuntimeError: If mpv is not available
        """
        if not MPV_AVAILABLE:
            raise RuntimeError(
                "python-mpv is not installed. Install it with: pip install python-mpv"
            )

        self.config = get_config()
        self.state: PlayerState = PlayerState.STOPPED
        self.volume: int = self.config.default_volume
        self.muted: bool = False
        self.current_station: Optional[Station] = None
        self.is_video_mode: bool = video_mode
        self._mpv: Optional[mpv.MPV] = None
        self._stream_url: Optional[str] = None
        self._on_state_change: Optional[Callable[[PlayerState], None]] = None

        logger.info(f"MPVPlayer initialized (video_mode={video_mode})")

    def _init_mpv(self) -> None:  # noqa: C901
        """
        Initialize the mpv player instance.

        This is called lazily when needed to avoid issues with initialization.
        """
        if self._mpv is not None:
            return

        try:
            logger.debug("Initializing mpv instance...")

            # MPV options
            mpv_options = {
                "ytdl": True,  # Enable yt-dlp integration
                "volume": self.volume,
                "cache": True,
                "cache_secs": 30,
                "demuxer_max_bytes": "50M",
                "demuxer_max_back_bytes": "30M",
                # Silence output to prevent UI interference
                "terminal": False,  # Don't use terminal output
                "msg_level": "all=no",  # Disable all messages
                "quiet": True,  # Quiet mode
            }

            if not self.is_video_mode:
                # Audio-only mode
                mpv_options.update(
                    {
                        "video": False,
                        "vo": "null",
                    }
                )
            else:
                # Video mode
                mpv_options.update(
                    {
                        "vo": "gpu",  # Use GPU for video output
                        "hwdec": "auto",  # Hardware decoding
                    }
                )

            self._mpv = mpv.MPV(**mpv_options)

            # Set up event observers
            @self._mpv.property_observer("pause")
            def on_pause_change(_name: str, value: bool) -> None:
                if value:
                    self._update_state(PlayerState.PAUSED)
                elif self.state != PlayerState.STOPPED:
                    self._update_state(PlayerState.PLAYING)

            @self._mpv.event_callback("start-file")
            def on_start_file(_event: dict) -> None:
                self._update_state(PlayerState.LOADING)
                logger.debug("Stream loading...")

            @self._mpv.event_callback("file-loaded")
            def on_file_loaded(_event: dict) -> None:
                self._update_state(PlayerState.PLAYING)
                logger.info("Stream loaded and playing")

            @self._mpv.event_callback("end-file")
            def on_end_file(event: dict) -> None:
                reason = event.get("reason", "unknown")
                logger.debug(f"Stream ended: {reason}")
                if reason == "error":
                    self._update_state(PlayerState.ERROR)
                elif reason != "stop":
                    self._update_state(PlayerState.STOPPED)

            logger.info("MPV instance initialized successfully")

        except Exception as e:
            logger.exception(f"Failed to initialize mpv: {e}")
            self._mpv = None
            raise RuntimeError(f"Failed to initialize mpv: {e}")

    def _update_state(self, new_state: PlayerState) -> None:
        """Update player state and notify callbacks."""
        old_state = self.state
        self.state = new_state

        if old_state != new_state:
            logger.debug(f"State changed: {old_state.value} -> {new_state.value}")
            if self._on_state_change:
                try:
                    self._on_state_change(new_state)
                except Exception as e:
                    logger.exception(f"Error in state change callback: {e}")

    def set_state_callback(self, callback: Callable[[PlayerState], None]) -> None:
        """
        Set a callback to be called when player state changes.

        Args:
            callback: Function that takes PlayerState as argument
        """
        self._on_state_change = callback

    def load_station(self, station: Station, fetch_stream: bool = True) -> None:
        """
        Load a station for playback.

        Args:
            station: The Station object to load
            fetch_stream: If True, fetch actual stream URL using yt-dlp

        Raises:
            ValueError: If station URL is invalid
            RuntimeError: If failed to fetch stream URL
        """
        if not station.url:
            raise ValueError("Station URL cannot be empty")

        self._init_mpv()

        self.current_station = station
        self.state = PlayerState.LOADING
        logger.info(f"Loading station: {station.name}")

        # For YouTube URLs, fetch the actual stream URL
        if "youtube.com" in station.url or "youtu.be" in station.url:
            if fetch_stream:
                logger.info("Fetching stream URL from YouTube...")
                fetcher = get_fetcher(prefer_audio_only=not self.is_video_mode)

                if not fetcher.check_yt_dlp_installed():
                    raise RuntimeError(
                        "yt-dlp is not installed. Install it with: pip install yt-dlp"
                    )

                stream_url = fetcher.get_stream_url(station.url)
                if not stream_url:
                    raise RuntimeError(f"Failed to fetch stream URL for {station.name}")

                self._stream_url = stream_url
                logger.info(f"Got stream URL: {stream_url[:50]}...")
            else:
                # Let mpv handle it with ytdl
                self._stream_url = station.url
        else:
            self._stream_url = station.url

    def play(self) -> None:
        """
        Start or resume playback.

        Raises:
            RuntimeError: If no station is loaded
        """
        if not self.current_station:
            raise RuntimeError("No station loaded")

        self._init_mpv()

        if self.state == PlayerState.PAUSED:
            # Resume from pause
            logger.info("Resuming playback")
            if self._mpv:
                self._mpv.pause = False
        else:
            # Start playback
            logger.info(f"Starting playback: {self.current_station.name}")
            if self._mpv and self._stream_url:
                try:
                    self._mpv.play(self._stream_url)
                    self._update_state(PlayerState.PLAYING)
                except Exception as e:
                    logger.exception(f"Failed to start playback: {e}")
                    self._update_state(PlayerState.ERROR)
                    raise RuntimeError(f"Failed to start playback: {e}")

    def pause(self) -> None:
        """Pause playback."""
        if self.state == PlayerState.PLAYING and self._mpv:
            logger.info("Pausing playback")
            self._mpv.pause = True

    def stop(self) -> None:
        """Stop playback."""
        if self.state in (PlayerState.PLAYING, PlayerState.PAUSED) and self._mpv:
            logger.info("Stopping playback")
            self._mpv.stop()
            self._update_state(PlayerState.STOPPED)

    def toggle_pause(self) -> None:
        """Toggle between play and pause."""
        if self.state == PlayerState.PLAYING:
            self.pause()
        elif self.state == PlayerState.PAUSED:
            self.play()

    def set_volume(self, volume: int) -> None:
        """
        Set playback volume.

        Args:
            volume: Volume level (0-100)

        Raises:
            ValueError: If volume is not in range 0-100
        """
        if not 0 <= volume <= 100:
            raise ValueError(f"Volume must be between 0 and 100, got {volume}")

        self.volume = volume
        logger.debug(f"Volume set to {volume}")

        if self._mpv:
            self._mpv.volume = volume

    def get_volume(self) -> int:
        """
        Get current volume level.

        Returns:
            Current volume (0-100)
        """
        return self.volume

    def volume_up(self, step: int = 5) -> None:
        """
        Increase volume.

        Args:
            step: Amount to increase (default: 5)
        """
        new_volume = min(100, self.volume + step)
        self.set_volume(new_volume)

    def volume_down(self, step: int = 5) -> None:
        """
        Decrease volume.

        Args:
            step: Amount to decrease (default: 5)
        """
        new_volume = max(0, self.volume - step)
        self.set_volume(new_volume)

    def toggle_mute(self) -> None:
        """Toggle mute on/off."""
        self.muted = not self.muted
        logger.debug(f"Mute: {self.muted}")

        if self._mpv:
            self._mpv.mute = self.muted

    def is_playing(self) -> bool:
        """
        Check if player is currently playing.

        Returns:
            True if playing, False otherwise
        """
        return self.state == PlayerState.PLAYING

    def get_state(self) -> PlayerState:
        """
        Get current player state.

        Returns:
            Current PlayerState
        """
        return self.state

    def get_time_pos(self) -> Optional[float]:
        """
        Get current playback position in seconds.

        Returns:
            Current position in seconds, or None if not playing
        """
        if self._mpv and self.state in (PlayerState.PLAYING, PlayerState.PAUSED):
            try:
                pos = self._mpv.time_pos
                return float(pos) if pos is not None else None
            except Exception:
                return None
        return None

    def get_duration(self) -> Optional[float]:
        """
        Get duration of current stream in seconds.

        Returns:
            Duration in seconds, or None if unavailable (e.g., live stream)
        """
        if self._mpv and self.state in (PlayerState.PLAYING, PlayerState.PAUSED):
            try:
                dur = self._mpv.duration
                return float(dur) if dur is not None else None
            except Exception:
                return None
        return None

    def is_live_stream(self) -> bool:
        """
        Check if current stream is a live stream.

        Returns:
            True if live stream, False otherwise
        """
        # Live streams typically don't have a duration
        duration = self.get_duration()
        return duration is None or duration == 0

    def cleanup(self) -> None:
        """
        Clean up player resources.

        Should be called when the player is no longer needed.
        """
        logger.info("Cleaning up player...")
        self.stop()

        if self._mpv:
            try:
                self._mpv.terminate()
            except Exception:  # nosec B110
                # Intentionally ignore errors during cleanup
                pass
            self._mpv = None

        logger.info("Player cleanup complete")

    def __del__(self) -> None:
        """Destructor to ensure cleanup."""
        self.cleanup()


# Global player instance
_player: Optional[MPVPlayer] = None


def get_player(video_mode: bool = False) -> MPVPlayer:
    """
    Get or create the global player instance.

    Args:
        video_mode: Whether to enable video mode

    Returns:
        MPVPlayer instance
    """
    global _player
    if _player is None:
        _player = MPVPlayer(video_mode=video_mode)
    return _player
