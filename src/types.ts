/**
 * Common types for LofiGirl Terminal
 */

export interface Station {
  id: string;
  name: string;
  url: string;
  description: string;
  genre: string;
}

export enum PlayerState {
  STOPPED = 'stopped',
  PLAYING = 'playing',
  PAUSED = 'paused',
  BUFFERING = 'buffering',
  LOADING = 'loading',
  ERROR = 'error',
}

export interface AppConfig {
  appName: string;
  logLevel: string;
  defaultVolume: number;
  audioQuality: string;
  defaultStation: string;
  theme: string;
  debugMode: boolean;
  showVisualizer: boolean;
  updateInterval: number;
  youtubeApiKey?: string;
}
