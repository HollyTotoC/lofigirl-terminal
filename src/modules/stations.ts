/**
 * Station management for LofiGirl Terminal
 */

import { Station } from '../types';

/**
 * Default lofi stations
 */
const DEFAULT_STATIONS: Station[] = [
  {
    id: 'lofi-hip-hop',
    name: 'Lofi Hip Hop Radio',
    url: 'https://www.youtube.com/watch?v=jfKfPfyJRdk',
    description: '24/7 chill lofi hip hop beats to study/relax to',
    genre: 'lofi-hip-hop',
  },
  {
    id: 'lofi-sleep',
    name: 'Lofi Sleep Radio',
    url: 'https://www.youtube.com/watch?v=rUxyKA_-grg',
    description: 'Calming lofi beats for sleep and meditation',
    genre: 'lofi-sleep',
  },
  {
    id: 'lofi-jazz',
    name: 'Lofi Jazz Radio',
    url: 'https://www.youtube.com/watch?v=Dx5qFachd3A',
    description: 'Smooth jazz with lofi aesthetics',
    genre: 'lofi-jazz',
  },
  {
    id: 'lofi-study',
    name: 'Lofi Study Radio',
    url: 'https://www.youtube.com/watch?v=f02mOEt11OQ',
    description: 'Focus-enhancing lofi beats for studying',
    genre: 'lofi-study',
  },
];

/**
 * Station Manager
 */
export class StationManager {
  private stations: Map<string, Station>;

  constructor() {
    this.stations = new Map();
    // Load default stations
    DEFAULT_STATIONS.forEach((station) => {
      this.stations.set(station.id, station);
    });
  }

  /**
   * Get all stations
   */
  getAllStations(): Station[] {
    return Array.from(this.stations.values());
  }

  /**
   * Get station by ID
   */
  getStation(id: string): Station | undefined {
    return this.stations.get(id);
  }

  /**
   * Add a new station
   */
  addStation(station: Station): void {
    this.stations.set(station.id, station);
  }

  /**
   * Remove a station
   */
  removeStation(id: string): boolean {
    return this.stations.delete(id);
  }

  /**
   * Check if station exists
   */
  hasStation(id: string): boolean {
    return this.stations.has(id);
  }
}

// Global station manager instance
let stationManager: StationManager | null = null;

export function getStationManager(): StationManager {
  if (!stationManager) {
    stationManager = new StationManager();
  }
  return stationManager;
}
