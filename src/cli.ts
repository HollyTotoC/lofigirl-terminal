/**
 * CLI interface for LofiGirl Terminal
 */

import { Command } from 'commander';
import chalk from 'chalk';
import Table from 'cli-table3';
import boxen from 'boxen';
import { getConfig } from './config';
import { getStationManager } from './modules/stations';
import { getPlayer } from './modules/player';
import { createLogger } from './logger';
import {
  checkYouTubeExtractor,
  checkMPV,
  getInstallInstructions,
} from './utils/dependencies';

const logger = createLogger('cli');
const VERSION = '0.2.0';

export function createCLI(): Command {
  const program = new Command();

  program
    .name('lofigirl')
    .description('🎵 LofiGirl Terminal - A terminal-based lofi radio player')
    .version(VERSION, '-v, --version', 'Output the current version')
    .option('-d, --debug', 'Enable debug mode');

  // Apply debug option globally
  program.hook('preAction', (thisCommand) => {
    const opts = thisCommand.opts();
    if (opts.debug) {
      process.env.LOG_LEVEL = 'DEBUG';
      logger.info('Debug mode enabled');
    }
  });

  /**
   * PLAY command
   */
  program
    .command('play')
    .description('🎧 Start playing a lofi radio station')
    .option('-s, --station <id>', 'Station ID to play')
    .option(
      '-v, --volume <level>',
      'Volume level (0-100)',
      (val) => parseInt(val, 10),
      undefined
    )
    .action(async (options) => {
      try {
        const config = getConfig();
        const stationManager = getStationManager();

        // Determine which station to play
        const stationId = options.station || config.defaultStation;

        // Get the station
        const station = stationManager.getStation(stationId);
        if (!station) {
          console.log(chalk.red.bold(`Error: Station '${stationId}' not found`));
          console.log(chalk.dim("\nUse 'lofigirl list' to see available stations"));
          process.exit(1);
        }

        // Create player and load station
        const player = getPlayer();
        if (options.volume !== undefined) {
          await player.setVolume(options.volume);
        }

        console.log(
          boxen(
            `${chalk.green.bold('Loading:')} ${station.name}\n${chalk.dim(station.description)}`,
            { padding: 1, borderColor: 'green' }
          )
        );

        await player.loadStation(station);
        await player.play();

        console.log(chalk.green.bold('\n▶ Playing'));
        console.log(`Volume: ${player.getVolume()}%`);
        console.log(
          chalk.dim(
            '\nNote: This is a demo. Actual audio playback requires MPV installed.'
          )
        );
        console.log(chalk.dim('Press Ctrl+C to stop'));

        // Wait for Ctrl+C
        process.on('SIGINT', async () => {
          console.log(chalk.yellow('\n\n⏹ Stopping...'));
          await player.stop();
          await player.cleanup();
          process.exit(0);
        });

        // Keep the process alive
        await new Promise(() => {});
      } catch (error) {
        console.log(chalk.red.bold(`Error: ${error}`));
        logger.error(`Error during playback: ${error}`);
        process.exit(1);
      }
    });

  /**
   * LIST command
   */
  program
    .command('list')
    .description('📻 List all available radio stations')
    .action(() => {
      const stationManager = getStationManager();
      const stations = stationManager.getAllStations();

      console.log(chalk.cyan.bold('\n✨ Available Lofi Radio Stations\n'));

      const table = new Table({
        head: [
          chalk.magenta.bold('ID'),
          chalk.magenta.bold('Name'),
          chalk.magenta.bold('Genre'),
          chalk.magenta.bold('Description'),
        ],
        colWidths: [20, 28, 18, 50],
        style: {
          head: [],
          border: ['gray'],
        },
      });

      stations.forEach((station) => {
        table.push([
          chalk.dim(station.id),
          chalk.cyan(station.name),
          chalk.green(station.genre),
          station.description,
        ]);
      });

      console.log(table.toString());
      console.log(
        chalk.dim("\n💡 Use 'lofigirl play --station <ID>' to play a station\n")
      );
    });

  /**
   * INFO command
   */
  program
    .command('info')
    .description('ℹ️  Show application information and configuration')
    .action(() => {
      const config = getConfig();

      console.log(chalk.cyan.bold('\n📊 LofiGirl Terminal Information\n'));

      const table = new Table({
        style: { head: [], border: ['gray'] },
        colWidths: [25, 40],
      });

      table.push(
        [chalk.bold('Version'), VERSION],
        [chalk.bold('App Name'), config.appName],
        [chalk.bold('Log Level'), config.logLevel],
        [chalk.bold('Default Volume'), `${config.defaultVolume}%`],
        [chalk.bold('Audio Quality'), config.audioQuality],
        [chalk.bold('Default Station'), config.defaultStation],
        [chalk.bold('Theme'), config.theme],
        [chalk.bold('Debug Mode'), config.debugMode.toString()]
      );

      console.log(table.toString());
      console.log();
    });

  /**
   * STATION-INFO command
   */
  program
    .command('station-info')
    .description('📡 Show detailed information about a station')
    .requiredOption('-s, --station <id>', 'Station ID')
    .action((options) => {
      const stationManager = getStationManager();
      const station = stationManager.getStation(options.station);

      if (!station) {
        console.log(chalk.red.bold(`Error: Station '${options.station}' not found`));
        process.exit(1);
      }

      console.log(chalk.cyan.bold(`\n${station.name}\n`));
      console.log(`${chalk.bold('ID:')} ${station.id}`);
      console.log(`${chalk.bold('Genre:')} ${station.genre}`);
      console.log(`${chalk.bold('Description:')} ${station.description}`);
      console.log(`${chalk.bold('URL:')} ${chalk.dim(station.url)}`);
      console.log();
    });

  /**
   * CHECK command
   */
  program
    .command('check')
    .description('🔍 Check if all required dependencies are installed')
    .action(() => {
      console.log(chalk.cyan.bold('\n🔍 Checking dependencies...\n'));

      const mpvCheck = checkMPV();
      const ytCheck = checkYouTubeExtractor();

      const table = new Table({
        head: [chalk.magenta.bold('Dependency'), chalk.magenta.bold('Status')],
        colWidths: [30, 20],
        style: {
          head: [],
          border: ['gray'],
        },
      });

      table.push(
        [
          'MPV media player',
          mpvCheck ? chalk.green.bold('✓ Installed') : chalk.red.bold('✗ Missing'),
        ],
        [
          'yt-dlp/youtube-dl',
          ytCheck.available
            ? chalk.green.bold(`✓ ${ytCheck.extractor}`)
            : chalk.red.bold('✗ Missing'),
        ]
      );

      console.log(table.toString());

      if (!mpvCheck || !ytCheck.available) {
        console.log(chalk.yellow(getInstallInstructions()));
      } else {
        console.log(
          chalk.green.bold(
            '\n✅ All dependencies are installed! You can use LofiGirl Terminal.\n'
          )
        );
        console.log(chalk.dim('Start with: lofigirl tui\n'));
      }
    });

  /**
   * TUI command
   */
  program
    .command('tui')
    .description('🎨 Launch the interactive TUI (Terminal User Interface)')
    .option(
      '--style <type>',
      'TUI style (rice=compact btop-style, classic=original)',
      'rice'
    )
    .action(async (_options) => {
      console.log(
        boxen(
          `${chalk.cyan.bold('🎵 Starting LofiGirl TUI')}\n\n${chalk.dim('Compact btop-style interface')}\n${chalk.dim("Press 'q' to quit")}`,
          { padding: 1, borderColor: 'cyan', margin: 1 }
        )
      );

      try {
        // Import TUI dynamically
        const { runTUI } = await import('./modules/tui');
        await runTUI();
      } catch (error) {
        console.log(
          chalk.red.bold('Error: Failed to start TUI\n') +
            chalk.yellow('Make sure all dependencies are installed: npm install')
        );
        logger.error(`Failed to start TUI: ${error}`);
        process.exit(1);
      }
    });

  return program;
}

/**
 * Run the CLI
 */
export async function runCLI(): Promise<void> {
  const program = createCLI();
  await program.parseAsync(process.argv);
}
