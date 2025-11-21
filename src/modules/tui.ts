/**
 * Terminal User Interface for LofiGirl Terminal
 * Using blessed for cross-platform TUI
 */

import blessed from 'blessed';
import { getPlayer } from './player';
import { getStationManager } from './stations';
import { PlayerState } from '../types';

export async function runTUI(_style = 'rice'): Promise<void> {
  // Create screen
  const screen = blessed.screen({
    smartCSR: true,
    title: 'LofiGirl Terminal',
    fullUnicode: true,
  });

  const stationManager = getStationManager();
  const player = getPlayer();
  const stations = stationManager.getAllStations();
  let currentStationIndex = 0;

  // Title box
  const titleBox = blessed.box({
    top: 0,
    left: 'center',
    width: '90%',
    height: 3,
    content: '{center}🎵 {bold}LofiGirl Terminal{/bold} - Lofi Radio Player{/center}',
    tags: true,
    border: {
      type: 'line',
    },
    style: {
      border: {
        fg: 'cyan',
      },
      fg: 'white',
    },
  });

  // Station info box
  const stationBox = blessed.box({
    top: 3,
    left: 'center',
    width: '90%',
    height: 5,
    tags: true,
    border: {
      type: 'line',
    },
    style: {
      border: {
        fg: 'green',
      },
    },
  });

  // Controls box
  const controlsBox = blessed.box({
    top: 8,
    left: 'center',
    width: '90%',
    height: 5,
    content: `{center}Controls:{/center}
{center}[SPACE] Play/Pause  [N] Next  [P] Previous  [M] Mute  [+/-] Volume  [Q] Quit{/center}`,
    tags: true,
    border: {
      type: 'line',
    },
    style: {
      border: {
        fg: 'yellow',
      },
    },
  });

  // Status box
  const statusBox = blessed.box({
    top: 13,
    left: 'center',
    width: '90%',
    height: 4,
    tags: true,
    border: {
      type: 'line',
    },
    style: {
      border: {
        fg: 'magenta',
      },
    },
  });

  // Log box
  const logBox = blessed.log({
    top: 17,
    left: 'center',
    width: '90%',
    height: 8,
    tags: true,
    scrollable: true,
    alwaysScroll: true,
    scrollbar: {
      ch: ' ',
      style: {
        bg: 'blue',
      },
    },
    border: {
      type: 'line',
    },
    style: {
      border: {
        fg: 'blue',
      },
    },
  });

  screen.append(titleBox);
  screen.append(stationBox);
  screen.append(controlsBox);
  screen.append(statusBox);
  screen.append(logBox);

  /**
   * Update station info display
   */
  function updateStationInfo(): void {
    const station = stations[currentStationIndex];
    stationBox.setContent(
      `{center}{bold}🎧 ${station.name}{/bold}{/center}\n` +
        `{center}{dim}Genre: ${station.genre}{/dim}{/center}`
    );
    screen.render();
  }

  /**
   * Update status display
   */
  function updateStatus(): void {
    const state = player.getState();
    const volume = player.getVolume();
    const stateIcon =
      state === PlayerState.PLAYING ? '▶️' : state === PlayerState.PAUSED ? '⏸️' : '⏹️';

    statusBox.setContent(
      `{center}Status: {bold}${stateIcon} ${state.toUpperCase()}{/bold}  |  Volume: {bold}${volume}%{/bold}{/center}`
    );
    screen.render();
  }

  /**
   * Log message to log box
   */
  function log(message: string, color = 'white'): void {
    logBox.log(`{${color}-fg}${message}{/${color}-fg}`);
  }

  /**
   * Load and play current station
   */
  async function playCurrentStation(): Promise<void> {
    const station = stations[currentStationIndex];
    try {
      log(`Loading ${station.name}...`, 'cyan');
      await player.loadStation(station);
      await player.play();
      updateStationInfo();
      updateStatus();
      log(`Now playing: ${station.name}`, 'green');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      log(`Error: ${errorMessage}`, 'red');
    }
  }

  /**
   * Next station
   */
  async function nextStation(): Promise<void> {
    currentStationIndex = (currentStationIndex + 1) % stations.length;
    await player.stop();
    await playCurrentStation();
  }

  /**
   * Previous station
   */
  async function previousStation(): Promise<void> {
    currentStationIndex = (currentStationIndex - 1 + stations.length) % stations.length;
    await player.stop();
    await playCurrentStation();
  }

  // Initialize
  updateStationInfo();
  updateStatus();
  log('Welcome to LofiGirl Terminal!', 'cyan');
  log('Press SPACE to start playing', 'yellow');

  // Keyboard controls
  screen.key(['space'], async () => {
    if (player.getState() === PlayerState.STOPPED) {
      await playCurrentStation();
    } else {
      await player.togglePause();
      updateStatus();
      log(player.isPlaying() ? 'Resumed playback' : 'Paused playback', 'yellow');
    }
  });

  screen.key(['n'], async () => {
    log('Next station...', 'cyan');
    await nextStation();
  });

  screen.key(['p'], async () => {
    log('Previous station...', 'cyan');
    await previousStation();
  });

  screen.key(['m'], async () => {
    await player.toggleMute();
    log('Mute toggled', 'yellow');
    updateStatus();
  });

  screen.key(['+', '='], async () => {
    await player.volumeUp(5);
    updateStatus();
    log(`Volume: ${player.getVolume()}%`, 'yellow');
  });

  screen.key(['-', '_'], async () => {
    await player.volumeDown(5);
    updateStatus();
    log(`Volume: ${player.getVolume()}%`, 'yellow');
  });

  screen.key(['q', 'C-c'], async () => {
    log('Shutting down...', 'red');
    await player.stop();
    await player.cleanup();
    process.exit(0);
  });

  // Update status every second
  setInterval(() => {
    updateStatus();
  }, 1000);

  screen.render();
}
