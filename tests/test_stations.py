"""Tests for the stations module."""

import pytest

from lofigirl_terminal.modules.stations import Station, StationManager


class TestStation:
    """Test suite for Station dataclass."""

    def test_station_creation(self) -> None:
        """Test creating a station instance."""
        station = Station(
            id="test-station",
            name="Test Station",
            url="https://example.com/stream",
            description="A test station",
            genre="lofi",
        )
        assert station.id == "test-station"
        assert station.name == "Test Station"
        assert station.url == "https://example.com/stream"
        assert station.description == "A test station"
        assert station.genre == "lofi"

    def test_station_string_representation(self) -> None:
        """Test station string representation."""
        station = Station(
            id="test",
            name="Test",
            url="http://test.com",
            description="Test description",
        )
        assert str(station) == "Test - Test description"


class TestStationManager:
    """Test suite for StationManager class."""

    def test_manager_initialization(self) -> None:
        """Test that manager initializes with default stations."""
        manager = StationManager()
        stations = manager.get_all_stations()
        assert len(stations) > 0
        assert all(isinstance(s, Station) for s in stations)

    def test_get_station_by_id(self) -> None:
        """Test retrieving a station by ID."""
        manager = StationManager()
        station = manager.get_station("lofi-hip-hop")
        assert station is not None
        assert station.id == "lofi-hip-hop"
        assert isinstance(station, Station)

    def test_get_nonexistent_station(self) -> None:
        """Test retrieving a nonexistent station returns None."""
        manager = StationManager()
        station = manager.get_station("nonexistent")
        assert station is None

    def test_get_all_stations(self) -> None:
        """Test getting all stations."""
        manager = StationManager()
        stations = manager.get_all_stations()
        assert isinstance(stations, list)
        assert len(stations) >= 4  # We have 4 default stations

    def test_add_custom_station(self) -> None:
        """Test adding a custom station."""
        manager = StationManager()
        custom_station = Station(
            id="custom",
            name="Custom Station",
            url="https://example.com/custom",
            description="A custom station",
        )
        manager.add_station(custom_station)

        retrieved = manager.get_station("custom")
        assert retrieved is not None
        assert retrieved.id == "custom"
        assert retrieved.name == "Custom Station"

    def test_add_duplicate_station_raises_error(self) -> None:
        """Test that adding a duplicate station ID raises an error."""
        manager = StationManager()
        duplicate = Station(
            id="lofi-hip-hop",  # Already exists
            name="Duplicate",
            url="http://example.com",
            description="Duplicate station",
        )
        with pytest.raises(ValueError, match="already exists"):
            manager.add_station(duplicate)

    def test_remove_station(self) -> None:
        """Test removing a station."""
        manager = StationManager()
        # Add a test station first
        test_station = Station(
            id="temp",
            name="Temp",
            url="http://test.com",
            description="Temporary",
        )
        manager.add_station(test_station)

        # Remove it
        result = manager.remove_station("temp")
        assert result is True
        assert manager.get_station("temp") is None

    def test_remove_nonexistent_station(self) -> None:
        """Test removing a nonexistent station returns False."""
        manager = StationManager()
        result = manager.remove_station("nonexistent")
        assert result is False

    def test_list_station_ids(self) -> None:
        """Test listing all station IDs."""
        manager = StationManager()
        ids = manager.list_station_ids()
        assert isinstance(ids, list)
        assert "lofi-hip-hop" in ids
        assert len(ids) >= 4
