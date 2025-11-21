/**
 * Application startup and initialization
 * Handles YouTube live stream scanning and station setup
 */

import { getConfig } from './config';
import { initStationManager } from './modules/stations';
import { scanLofiGirlLiveStreamsWithFallback } from './modules/youtube-scanner';
import { logger } from './logger';
import chalk from 'chalk';

/**
 * Initialize the application
 * - Scans YouTube for live streams
 * - Initializes StationManager with scanned or default stations
 */
export async function initializeApp(): Promise<void> {
  try {
    logger.info('Initializing LofiGirl Terminal...');

    const config = getConfig();

    // Scan for live streams
    logger.info('Scanning for live YouTube streams...');
    const liveStations = await scanLofiGirlLiveStreamsWithFallback(config.youtubeApiKey);

    if (liveStations.length > 0) {
      // Initialize with scanned live stations
      logger.info(`Found ${liveStations.length} live streams, using them as stations`);
      initStationManager(liveStations);

      // Show info to user if debug mode
      if (config.debugMode) {
        console.log(chalk.green(`✓ Loaded ${liveStations.length} live streams from @LofiGirl`));
        liveStations.forEach((station, index) => {
          console.log(chalk.dim(`  ${index + 1}. ${station.name}`));
        });
      }
    } else {
      // Fallback to default stations
      logger.warn('No live streams found, falling back to default stations');
      initStationManager();

      if (config.debugMode) {
        console.log(chalk.yellow('⚠ No live streams found, using default stations'));
      }
    }

    logger.info('Application initialized successfully');
  } catch (error: any) {
    logger.error(`Failed to initialize app: ${error.message}`);

    // Always fallback to default stations on error
    logger.warn('Falling back to default stations due to initialization error');
    initStationManager();

    if (getConfig().debugMode) {
      console.log(chalk.yellow('⚠ Initialization failed, using default stations'));
      console.log(chalk.dim(`  Error: ${error.message}`));
    }
  }
}
