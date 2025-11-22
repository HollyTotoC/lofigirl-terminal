/**
 * MPV Audio Player for LofiGirl Terminal
 */

import mpv from 'node-mpv';
import { Station, PlayerState } from '../types';
import { createLogger } from '../logger';
import { getConfig } from '../config';
import { checkYouTubeExtractor, checkMPV } from '../utils/dependencies';

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
  private isIntentionalStop = false;
  private restartAttempts = 0;
  private readonly MAX_RESTART_ATTEMPTS = 3;

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

      // Check if MPV is available
      if (!checkMPV()) {
        throw new Error(
          'MPV media player not found. Please install MPV to use LofiGirl Terminal.\n' +
            'Installation: https://mpv.io/installation/'
        );
      }

      // Check if YouTube extractor is available (for YouTube URLs)
      const ytCheck = checkYouTubeExtractor();
      if (!ytCheck.available) {
        logger.warn(
          'yt-dlp/youtube-dl not found. YouTube streaming may not work. ' +
            'Install yt-dlp for YouTube support: pip install yt-dlp'
        );
      } else {
        logger.debug(`Using YouTube extractor: ${ytCheck.extractor}`);
      }

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const mpvOptions: any = {
        audio_only: !this.isVideoMode,
        time_update: 1,
        verbose: config.debugMode,
        // Enable YouTube support via yt-dlp/youtube-dl
        ytdl: true,
        'ytdl-format': 'bestaudio',
        // Stream buffering and caching options for live streams
        cache: 'yes',
        'cache-secs': 120,
        'demuxer-max-bytes': '50M',
        'demuxer-max-back-bytes': '25M',
        'network-timeout': 60,
        // Keep connection alive
        'keep-open': 'yes',
        'stream-lavf-o': 'reconnect=1,reconnect_streamed=1,reconnect_delay_max=5',
      };

      // Only set ytdl_path if we detected a specific extractor
      // This allows MPV to use its default behavior when neither is specified,
      // or use the correct extractor when one is detected
      if (ytCheck.available && ytCheck.extractor) {
        mpvOptions['script-opts'] = `ytdl_hook-ytdl_path=${ytCheck.extractor}`;
        logger.debug(`Configured MPV to use: ${ytCheck.extractor}`);
      }

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
        this.restartAttempts = 0; // Reset on successful start
        this.updateState(PlayerState.PLAYING);
      });

      this.mpvPlayer.on('paused', () => {
        logger.debug('MPV player paused');
        this.updateState(PlayerState.PAUSED);
      });

      this.mpvPlayer.on('stopped', () => {
        logger.debug('MPV player stopped');
        const wasPlaying = this.state === PlayerState.PLAYING;
        this.updateState(PlayerState.STOPPED);

        // Auto-restart if stream stopped unexpectedly while playing (not intentional stop)
        if (
          wasPlaying &&
          this.currentStation &&
          !this.isIntentionalStop &&
          this.restartAttempts < this.MAX_RESTART_ATTEMPTS
        ) {
          this.restartAttempts++;
          logger.info(
            `Stream stopped unexpectedly, attempting to restart (${this.restartAttempts}/${this.MAX_RESTART_ATTEMPTS})...`
          );
          setTimeout(() => {
            if (this.currentStation) {
              this.play().catch((error) => {
                logger.error(`Failed to restart stream: ${error.message}`);
              });
            }
          }, 2000 * this.restartAttempts); // exponential backoff
        }
      });

      this.mpvPlayer.on('timeposition', (time: number) => {
        logger.debug(`Playback position: ${time}s`);
      });

      await this.mpvPlayer.start();
      await this.mpvPlayer.volume(this.volume);

      logger.info('MPV instance initialized successfully');
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : JSON.stringify(error);
      logger.error(`Failed to initialize mpv: ${errorMessage}`);
      throw new Error(`Failed to initialize mpv: ${errorMessage}`);
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
      this.updateState(PlayerState.PLAYING);
    } else {
      logger.info(`Starting playback: ${this.currentStation.name}`);
      try {
        await this.mpvPlayer.load(this.currentStation.url);
        this.updateState(PlayerState.PLAYING);
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : JSON.stringify(error);
        logger.error(`Failed to start playback: ${errorMessage}`);
        this.updateState(PlayerState.ERROR);
        throw new Error(`Failed to start playback: ${errorMessage}`);
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
      this.isIntentionalStop = true;
      await this.mpvPlayer.stop();
      this.updateState(PlayerState.STOPPED);
      this.isIntentionalStop = false;
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
   * Check if muted
   */
  isMuted(): boolean {
    return this.muted;
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
