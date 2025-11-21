/**
 * Terminal User Interface for LofiGirl Terminal
 * Rice-style compact UI with ASCII art
 */

import blessed from 'blessed';
import { getPlayer } from './player';
import { getStationManager } from './stations';
import { PlayerState } from '../types';
import { enableTUIMode } from '../logger';

// ASCII Art for lofi vibes
const LOFI_ASCII = `
     ▄▄▄▄▄▄▄▄▄
    █░░░░░░░░█
    █░ ◉  ◉ ░█   ♪♫♪
    █░   ▿   ░█
    █░ ╰───╯ ░█
     ▀▀▀▀▀▀▀▀▀
`;

const WAVE_FRAMES = [
  '▁▂▃▄▅▆▇█',
  '▂▃▄▅▆▇█▁',
  '▃▄▅▆▇█▁▂',
  '▄▅▆▇█▁▂▃',
  '▅▆▇█▁▂▃▄',
  '▆▇█▁▂▃▄▅',
  '▇█▁▂▃▄▅▆',
  '█▁▂▃▄▅▆▇',
];

export async function runTUI(): Promise<void> {
  // Enable TUI mode to suppress console logs
  enableTUIMode();

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
  let waveFrame = 0;
  let lastPlayerState = PlayerState.STOPPED;

  // ╔══════════════════════════════════════╗
  // ║  COMPACT RICE-STYLE LAYOUT           ║
  // ╚══════════════════════════════════════╝

  // Top bar with ASCII art and title (compact)
  const headerBox = blessed.box({
    top: 0,
    left: 0,
    width: '100%',
    height: 8,
    tags: true,
    border: {
      type: 'line',
    },
    style: {
      fg: 'magenta',
      bg: 'black',
      border: {
        fg: 'magenta',
      },
    },
  });

  // Player info - compact single box
  const playerBox = blessed.box({
    top: 8,
    left: 0,
    width: '100%',
    height: 7,
    tags: true,
    border: {
      type: 'line',
    },
    style: {
      fg: 'cyan',
      bg: 'black',
      border: {
        fg: 'cyan',
      },
    },
  });

  // Controls - single line compact
  const controlsBox = blessed.box({
    top: 15,
    left: 0,
    width: '100%',
    height: 3,
    tags: true,
    border: {
      type: 'line',
    },
    style: {
      fg: 'green',
      bg: 'black',
      border: {
        fg: 'green',
      },
    },
  });

  // Logs - minimal, at bottom
  const logBox = blessed.log({
    top: 18,
    left: 0,
    width: '100%',
    height: 'shrink',
    tags: true,
    scrollable: true,
    alwaysScroll: true,
    mouse: true,
    keys: true,
    vi: true,
    scrollbar: {
      ch: '█',
      style: {
        fg: 'magenta',
        bg: 'black',
      },
    },
    border: {
      type: 'line',
    },
    style: {
      fg: 'magenta',
      bg: 'black',
      border: {
        fg: 'magenta',
      },
    },
  });

  screen.append(headerBox);
  screen.append(playerBox);
  screen.append(controlsBox);
  screen.append(logBox);

  /**
   * Update header with ASCII art and title
   */
  function updateHeader(): void {
    const title = '{center}{bold}{magenta-fg}♪ LofiGirl Terminal ♪{/}{/bold}{/center}';
    const subtitle = '{center}{white-fg}chill beats to code/relax to{/}{/center}';

    headerBox.setContent(`${title}\n${subtitle}\n${LOFI_ASCII}`);
    screen.render();
  }

  /**
   * Update player info display (compact)
   */
  function updatePlayerInfo(): void {
    if (stations.length === 0) {
      playerInfoBox.setContent('{center}{red-fg}No stations available.{/red-fg}{/center}');
      screen.render();
      return;
    }
    const station = stations[currentStationIndex];
    const state = player.getState();
    const volume = player.getVolume();
    const isMuted = player.isMuted();

    // State icon with color
    let stateDisplay = '';
    if (state === PlayerState.PLAYING) {
      stateDisplay = '{green-fg}▶ PLAYING{/}';
    } else if (state === PlayerState.PAUSED) {
      stateDisplay = '{yellow-fg}⏸ PAUSED{/}';
    } else {
      stateDisplay = '{white-fg}⏹ STOPPED{/}';
    }

    // Volume bar
    const volBars = Math.max(0, Math.min(10, Math.floor(volume / 10)));
    const volBar = '█'.repeat(volBars) + '░'.repeat(10 - volBars);
    const volDisplay = isMuted
      ? '{red-fg}🔇 MUTED{/}'
      : `{cyan-fg}🔊 ${volBar}{/} {bold}${volume}%{/bold}`;

    // Wave animation
    const wave = state === PlayerState.PLAYING ? WAVE_FRAMES[waveFrame] : '▁▁▁▁▁▁▁▁';

    const content = `
 {center}{bold}{magenta-fg}╭─────────────────────────────────────────╮{/}{/bold}{/center}
 {center}{bold}{magenta-fg}${station.name}{/}{/bold}{/center}
 {center}{white-fg}${station.genre} • ${station.description}{/}{/center}
 {center}${stateDisplay}  │  ${volDisplay}{/center}
 {center}{cyan-fg}${wave}{/}{/center}`;

    playerBox.setContent(content);
    screen.render();
  }

  /**
   * Update controls display (compact)
   */
  function updateControls(): void {
    const controls =
      '{center}{green-fg}[SPACE]{/} Play/Pause  {green-fg}[N]{/} Next  {green-fg}[P]{/} Prev  {green-fg}[M]{/} Mute  {green-fg}[+/-]{/} Vol  {red-fg}[Q]{/} Quit{/center}';
    controlsBox.setContent(controls);
    screen.render();
  }

  /**
   * Log message to log box (with colors)
   */
  function log(
    message: string,
    type: 'info' | 'success' | 'warn' | 'error' = 'info'
  ): void {
    const timestamp = new Date().toLocaleTimeString('en-US', { hour12: false });
    let color = 'magenta';

    switch (type) {
      case 'success':
        color = 'green';
        break;
      case 'warn':
        color = 'yellow';
        break;
      case 'error':
        color = 'red';
        break;
    }

    logBox.log(`{white-fg}${timestamp}{/} {${color}-fg}${message}{/}`);
  }

  /**
   * Load and play current station
   */
  async function playCurrentStation(): Promise<void> {
    if (!stations || stations.length === 0) {
      log('No stations available to play.', 'error');
      return;
    }
    const station = stations[currentStationIndex];
    try {
      log(`Loading ${station.name}...`, 'info');
      await player.loadStation(station);
      await player.play();
      updateHeader();
      updatePlayerInfo();
      log(`♪ Now playing: ${station.name}`, 'success');
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      log(`Error: ${errorMessage}`, 'error');
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

  // Initialize UI
  updateHeader();
  updatePlayerInfo();
  updateControls();
  log('Welcome to LofiGirl Terminal! ♪', 'success');
  log('Press SPACE to start playing...', 'info');

  // ╔══════════════════════════════════════╗
  // ║  KEYBOARD CONTROLS                   ║
  // ╚══════════════════════════════════════╝

  screen.key(['space'], async () => {
    if (player.getState() === PlayerState.STOPPED) {
      await playCurrentStation();
    } else {
      await player.togglePause();
      updatePlayerInfo();
      log(player.isPlaying() ? '▶ Resumed' : '⏸ Paused', 'warn');
    }
  });

  screen.key(['n'], async () => {
    log('→ Next station', 'info');
    await nextStation();
  });

  screen.key(['p'], async () => {
    log('← Previous station', 'info');
    await previousStation();
  });

  screen.key(['m'], async () => {
    await player.toggleMute();
    log(player.isMuted() ? '🔇 Muted' : '🔊 Unmuted', 'warn');
    updatePlayerInfo();
  });

  screen.key(['+', '='], async () => {
    await player.volumeUp(5);
    updatePlayerInfo();
  });

  screen.key(['-', '_'], async () => {
    await player.volumeDown(5);
    updatePlayerInfo();
  });

  screen.key(['q', 'C-c'], async () => {
    log('Shutting down... Goodbye! ♪', 'error');
    await player.stop();
    await player.cleanup();
    process.exit(0);
  });

  // ╔══════════════════════════════════════╗
  // ║  ANIMATIONS & UPDATES                ║
  // ╚══════════════════════════════════════╝

  // Update wave animation and status - optimized to reduce unnecessary re-renders
  setInterval(() => {
    const currentState = player.getState();
    const stateChanged = currentState !== lastPlayerState;

    // Only update wave animation when playing
    if (currentState === PlayerState.PLAYING) {
      waveFrame = (waveFrame + 1) % WAVE_FRAMES.length;
      // Always update during playback for smooth animation
      updatePlayerInfo();
    } else if (stateChanged) {
      // Update only when state changes (stopped/paused/etc)
      updatePlayerInfo();
    }

    lastPlayerState = currentState;
  }, 200);

  screen.render();
}
