/**
 * MPV Audio Player for LofiGirl Terminal
 */

import mpv from 'node-mpv';
import { Station, PlayerState } from '../types';
import { createLogger } from '../logger';
import { getConfig } from '../config';

const logger = createLogger('player');
const config = getConfig();

export class MPVPlayer {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  private mpvPlayer: any;
  private state: PlayerState;
  private volume: number;
  private muted: boolean;
  private currentStation: Station | null;
  private isVideoMode: boolean;

  constructor(videoMode = false) {
    this.state = PlayerState.STOPPED;
    this.volume = config.defaultVolume;
    this.muted = false;
    this.currentStation = null;
    this.isVideoMode = videoMode;
    this.mpvPlayer = null;

    logger.info(`MPVPlayer initialized (video_mode=${videoMode})`);
  }

  /**
   * Initialize MPV player instance
   */
  private async initMPV(): Promise<void> {
    if (this.mpvPlayer) {
      return;
    }

    try {
      logger.debug('Initializing mpv instance...');

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const mpvOptions: any = {
        audio_only: !this.isVideoMode,
        time_update: 1,
        verbose: config.debugMode,
      };

      // Try different socket paths for cross-platform compatibility
      if (process.platform === 'win32') {
        mpvOptions.socket = '\\\\.\\pipe\\mpvsocket';
      } else {
        mpvOptions.socket = '/tmp/mpvsocket';
      }

      this.mpvPlayer = new mpv(mpvOptions);

      // Set up event listeners
      this.mpvPlayer.on('started', () => {
        logger.debug('MPV player started');
        this.updateState(PlayerState.PLAYING);
      });

      this.mpvPlayer.on('paused', () => {
        logger.debug('MPV player paused');
        this.updateState(PlayerState.PAUSED);
      });

      this.mpvPlayer.on('stopped', () => {
        logger.debug('MPV player stopped');
        this.updateState(PlayerState.STOPPED);
      });

      this.mpvPlayer.on('timeposition', (time: number) => {
        logger.debug(`Playback position: ${time}s`);
      });

      await this.mpvPlayer.start();
      await this.mpvPlayer.volume(this.volume);

      logger.info('MPV instance initialized successfully');
    } catch (error) {
      logger.error(`Failed to initialize mpv: ${error}`);
      throw new Error(`Failed to initialize mpv: ${error}`);
    }
  }

  /**
   * Update player state
   */
  private updateState(newState: PlayerState): void {
    const oldState = this.state;
    this.state = newState;

    if (oldState !== newState) {
      logger.debug(`State changed: ${oldState} -> ${newState}`);
    }
  }

  /**
   * Load a station for playback
   */
  async loadStation(station: Station): Promise<void> {
    if (!station.url) {
      throw new Error('Station URL cannot be empty');
    }

    await this.initMPV();

    this.currentStation = station;
    this.updateState(PlayerState.LOADING);
    logger.info(`Loading station: ${station.name}`);
  }

  /**
   * Start or resume playback
   */
  async play(): Promise<void> {
    if (!this.currentStation) {
      throw new Error('No station loaded');
    }

    await this.initMPV();

    if (this.state === PlayerState.PAUSED) {
      logger.info('Resuming playback');
      await this.mpvPlayer.resume();
    } else {
      logger.info(`Starting playback: ${this.currentStation.name}`);
      try {
        await this.mpvPlayer.load(this.currentStation.url);
        this.updateState(PlayerState.PLAYING);
      } catch (error) {
        logger.error(`Failed to start playback: ${error}`);
        this.updateState(PlayerState.ERROR);
        throw error;
      }
    }
  }

  /**
   * Pause playback
   */
  async pause(): Promise<void> {
    if (this.state === PlayerState.PLAYING && this.mpvPlayer) {
      logger.info('Pausing playback');
      await this.mpvPlayer.pause();
    }
  }

  /**
   * Stop playback
   */
  async stop(): Promise<void> {
    if (
      (this.state === PlayerState.PLAYING || this.state === PlayerState.PAUSED) &&
      this.mpvPlayer
    ) {
      logger.info('Stopping playback');
      await this.mpvPlayer.stop();
      this.updateState(PlayerState.STOPPED);
    }
  }

  /**
   * Toggle between play and pause
   */
  async togglePause(): Promise<void> {
    if (this.state === PlayerState.PLAYING) {
      await this.pause();
    } else if (this.state === PlayerState.PAUSED) {
      await this.play();
    }
  }

  /**
   * Set volume (0-100)
   */
  async setVolume(volume: number): Promise<void> {
    if (volume < 0 || volume > 100) {
      throw new Error(`Volume must be between 0 and 100, got ${volume}`);
    }

    this.volume = volume;
    logger.debug(`Volume set to ${volume}`);

    if (this.mpvPlayer) {
      await this.mpvPlayer.volume(volume);
    }
  }

  /**
   * Get current volume
   */
  getVolume(): number {
    return this.volume;
  }

  /**
   * Increase volume
   */
  async volumeUp(step = 5): Promise<void> {
    const newVolume = Math.min(100, this.volume + step);
    await this.setVolume(newVolume);
  }

  /**
   * Decrease volume
   */
  async volumeDown(step = 5): Promise<void> {
    const newVolume = Math.max(0, this.volume - step);
    await this.setVolume(newVolume);
  }

  /**
   * Toggle mute
   */
  async toggleMute(): Promise<void> {
    this.muted = !this.muted;
    logger.debug(`Mute: ${this.muted}`);

    if (this.mpvPlayer) {
      await this.mpvPlayer.mute(this.muted);
    }
  }

  /**
   * Check if playing
   */
  isPlaying(): boolean {
    return this.state === PlayerState.PLAYING;
  }

  /**
   * Get current state
   */
  getState(): PlayerState {
    return this.state;
  }

  /**
   * Get current playback time
   */
  async getTimePos(): Promise<number | null> {
    if (
      this.mpvPlayer &&
      (this.state === PlayerState.PLAYING || this.state === PlayerState.PAUSED)
    ) {
      try {
        const pos = await this.mpvPlayer.getTimePosition();
        return pos || null;
      } catch {
        return null;
      }
    }
    return null;
  }

  /**
   * Cleanup resources
   */
  async cleanup(): Promise<void> {
    logger.info('Cleaning up player...');
    await this.stop();

    if (this.mpvPlayer) {
      try {
        await this.mpvPlayer.quit();
      } catch {
        // Ignore errors during cleanup
      }
      this.mpvPlayer = null;
    }

    logger.info('Player cleanup complete');
  }
}

// Global player instance
let playerInstance: MPVPlayer | null = null;

export function getPlayer(videoMode = false): MPVPlayer {
  if (!playerInstance) {
    playerInstance = new MPVPlayer(videoMode);
  }
  return playerInstance;
}
