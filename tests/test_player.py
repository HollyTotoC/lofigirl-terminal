"""Tests for the player module."""

import pytest

from lofigirl_terminal.modules.player import AudioPlayer, PlayerState
from lofigirl_terminal.modules.stations import Station


class TestPlayerState:
    """Test suite for PlayerState enum."""

    def test_player_states_exist(self) -> None:
        """Test that all player states are defined."""
        assert PlayerState.STOPPED
        assert PlayerState.PLAYING
        assert PlayerState.PAUSED
        assert PlayerState.BUFFERING
        assert PlayerState.ERROR

    def test_player_state_values(self) -> None:
        """Test player state values."""
        assert PlayerState.STOPPED.value == "stopped"
        assert PlayerState.PLAYING.value == "playing"
        assert PlayerState.PAUSED.value == "paused"


class TestAudioPlayer:
    """Test suite for AudioPlayer class."""

    @pytest.fixture
    def player(self) -> AudioPlayer:
        """Create an AudioPlayer instance for testing."""
        return AudioPlayer()

    @pytest.fixture
    def test_station(self) -> Station:
        """Create a test station."""
        return Station(
            id="test",
            name="Test Station",
            url="https://example.com/stream",
            description="Test",
        )

    def test_player_initialization(self, player: AudioPlayer) -> None:
        """Test player initializes correctly."""
        assert player.state == PlayerState.STOPPED
        assert player.current_station is None
        assert 0 <= player.volume <= 100

    def test_load_station(self, player: AudioPlayer, test_station: Station) -> None:
        """Test loading a station."""
        player.load_station(test_station)
        assert player.current_station == test_station
        assert player.state == PlayerState.STOPPED

    def test_load_station_invalid_url(self, player: AudioPlayer) -> None:
        """Test loading a station with invalid URL raises error."""
        invalid_station = Station(
            id="invalid",
            name="Invalid",
            url="",  # Empty URL
            description="Invalid station",
        )
        with pytest.raises(ValueError, match="URL cannot be empty"):
            player.load_station(invalid_station)

    def test_play_without_station(self, player: AudioPlayer) -> None:
        """Test playing without loading a station raises error."""
        with pytest.raises(RuntimeError, match="No station loaded"):
            player.play()

    def test_play(self, player: AudioPlayer, test_station: Station) -> None:
        """Test playing a station."""
        player.load_station(test_station)
        player.play()
        assert player.state == PlayerState.PLAYING
        assert player.is_playing()

    def test_pause(self, player: AudioPlayer, test_station: Station) -> None:
        """Test pausing playback."""
        player.load_station(test_station)
        player.play()
        player.pause()
        assert player.state == PlayerState.PAUSED
        assert not player.is_playing()

    def test_resume_after_pause(
        self, player: AudioPlayer, test_station: Station
    ) -> None:
        """Test resuming after pause."""
        player.load_station(test_station)
        player.play()
        player.pause()
        player.play()  # Resume
        assert player.state == PlayerState.PLAYING

    def test_stop(self, player: AudioPlayer, test_station: Station) -> None:
        """Test stopping playback."""
        player.load_station(test_station)
        player.play()
        player.stop()
        assert player.state == PlayerState.STOPPED
        assert not player.is_playing()

    def test_set_volume(self, player: AudioPlayer) -> None:
        """Test setting volume."""
        player.set_volume(75)
        assert player.get_volume() == 75

        player.set_volume(0)
        assert player.get_volume() == 0

        player.set_volume(100)
        assert player.get_volume() == 100

    def test_set_invalid_volume(self, player: AudioPlayer) -> None:
        """Test setting invalid volume raises error."""
        with pytest.raises(ValueError, match="must be between 0 and 100"):
            player.set_volume(150)

        with pytest.raises(ValueError):
            player.set_volume(-10)

    def test_get_state(self, player: AudioPlayer, test_station: Station) -> None:
        """Test getting player state."""
        assert player.get_state() == PlayerState.STOPPED

        player.load_station(test_station)
        player.play()
        assert player.get_state() == PlayerState.PLAYING

        player.pause()
        assert player.get_state() == PlayerState.PAUSED

    def test_cleanup(self, player: AudioPlayer, test_station: Station) -> None:
        """Test cleanup stops player."""
        player.load_station(test_station)
        player.play()
        player.cleanup()
        assert player.state == PlayerState.STOPPED
