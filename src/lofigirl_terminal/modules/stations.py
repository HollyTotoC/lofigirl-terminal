"""
Radio station management for LofiGirl Terminal.

This module handles the configuration and management of lofi radio stations.
Currently uses placeholder URLs that should be replaced with actual streaming URLs.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from lofigirl_terminal.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Station:
    """
    Represents a radio station.

    Attributes:
        id: Unique identifier for the station
        name: Display name of the station
        url: Streaming URL
        description: Brief description of the station
        genre: Music genre
    """

    id: str
    name: str
    url: str
    description: str
    genre: str = "lofi"

    def __str__(self) -> str:
        """Return string representation of the station."""
        return f"{self.name} - {self.description}"


class StationManager:
    """
    Manages available radio stations.

    This class provides methods to retrieve and manage radio stations,
    including adding custom stations and getting station information.
    """

    def __init__(self) -> None:
        """Initialize the station manager with default stations."""
        self._stations: Dict[str, Station] = {}
        self._load_default_stations()

    def _load_default_stations(self) -> None:
        """
        Load default LofiGirl radio stations from YouTube.

        These are the official LofiGirl YouTube live streams.
        URLs will be resolved at runtime using yt-dlp to get the actual
        streaming URLs.
        """
        default_stations = [
            Station(
                id="lofi-hip-hop",
                name="📚 Lofi Hip Hop Radio - Beats to Relax/Study",
                url="https://www.youtube.com/watch?v=jfKfPfyJRdk",
                description="24/7 chill lofi hip hop beats to study/relax to",
                genre="lofi-hip-hop",
            ),
            Station(
                id="lofi-sleep",
                name="💤 Lofi Hip Hop Radio - Beats to Sleep/Chill",
                url="https://www.youtube.com/@LofiGirl/streams",  # Main channel
                description="Calming lofi beats for sleep and meditation",
                genre="lofi-sleep",
            ),
            Station(
                id="synthwave",
                name="🌌 Synthwave Radio - Beats to Chill/Game",
                url="https://www.youtube.com/@LofiGirl/streams",
                description="Retro synthwave beats perfect for gaming",
                genre="synthwave",
            ),
            Station(
                id="lofi-jazz",
                name="🎷 Jazz Lofi Radio - Beats to Chill/Study",
                url="https://www.youtube.com/@LofiGirl/streams",
                description="Smooth jazz with lofi aesthetics",
                genre="lofi-jazz",
            ),
        ]

        for station in default_stations:
            self._stations[station.id] = station
            logger.debug(f"Loaded station: {station.name}")

    def get_station(self, station_id: str) -> Optional[Station]:
        """
        Get a station by its ID.

        Args:
            station_id: Unique identifier of the station

        Returns:
            Station object if found, None otherwise

        Example:
            >>> manager = StationManager()
            >>> station = manager.get_station("lofi-hip-hop")
            >>> print(station.name)
            Lofi Hip Hop Radio
        """
        station = self._stations.get(station_id)
        if station:
            logger.debug(f"Retrieved station: {station.name}")
        else:
            logger.warning(f"Station not found: {station_id}")
        return station

    def get_all_stations(self) -> List[Station]:
        """
        Get all available stations.

        Returns:
            List of all Station objects

        Example:
            >>> manager = StationManager()
            >>> stations = manager.get_all_stations()
            >>> for station in stations:
            ...     print(station.name)
        """
        return list(self._stations.values())

    def add_station(self, station: Station) -> None:
        """
        Add a custom station.

        Args:
            station: Station object to add

        Raises:
            ValueError: If station ID already exists

        Example:
            >>> manager = StationManager()
            >>> custom = Station(
            ...     id="my-station",
            ...     name="My Custom Station",
            ...     url="https://example.com/stream",
            ...     description="My personal lofi station"
            ... )
            >>> manager.add_station(custom)
        """
        if station.id in self._stations:
            raise ValueError(f"Station with ID '{station.id}' already exists")

        self._stations[station.id] = station
        logger.info(f"Added custom station: {station.name}")

    def remove_station(self, station_id: str) -> bool:
        """
        Remove a station.

        Args:
            station_id: ID of the station to remove

        Returns:
            True if station was removed, False if not found

        Example:
            >>> manager = StationManager()
            >>> manager.remove_station("lofi-hip-hop")
            True
        """
        if station_id in self._stations:
            station = self._stations.pop(station_id)
            logger.info(f"Removed station: {station.name}")
            return True
        logger.warning(f"Cannot remove station: {station_id} not found")
        return False

    def list_station_ids(self) -> List[str]:
        """
        Get list of all station IDs.

        Returns:
            List of station IDs

        Example:
            >>> manager = StationManager()
            >>> ids = manager.list_station_ids()
            >>> print(ids)
            ['lofi-hip-hop', 'lofi-jazz', 'lofi-sleep', 'lofi-study']
        """
        return list(self._stations.keys())
