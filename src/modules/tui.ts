/**
 * Terminal User Interface for LofiGirl Terminal
 * Modern, clean design inspired by bottom with Catppuccin Mocha theme
 */

import blessed from 'blessed';
import { getPlayer } from './player';
import { getStationManager } from './stations';
import { PlayerState } from '../types';
import { enableTUIMode, disableTUIMode } from '../logger';

// ═══════════════════════════════════════════════════════════════════════════
// CATPPUCCIN MOCHA COLOR PALETTE
// ═══════════════════════════════════════════════════════════════════════════
const CATPPUCCIN_MOCHA = {
  rosewater: '#f5e0dc',
  flamingo: '#f2cdcd',
  pink: '#f5c2e7',
  mauve: '#cba6f7',
  red: '#f38ba8',
  maroon: '#eba0ac',
  peach: '#fab387',
  yellow: '#f9e2af',
  green: '#a6e3a1',
  teal: '#94e2d5',
  sky: '#89dceb',
  sapphire: '#74c7ec',
  blue: '#89b4fa',
  lavender: '#b4befe',
  text: '#cdd6f4',
  subtext1: '#bac2de',
  subtext0: '#a6adc8',
  overlay2: '#9399b2',
  overlay1: '#7f849c',
  overlay0: '#6c7086',
  surface2: '#585b70',
  surface1: '#45475a',
  surface0: '#313244',
  base: '#1e1e2e',
  mantle: '#181825',
  crust: '#11111b',
};

// Blessed color mapping (closest matches)
const THEME = {
  bg: 'black', // Closest to base
  fg: 'white', // Closest to text
  primary: 'magenta', // mauve
  secondary: 'cyan', // sapphire
  success: 'green', // green
  warning: 'yellow', // yellow
  error: 'red', // red
  accent: 'blue', // lavender
  muted: 'gray', // overlay0
  border: '#45475a', // surface1
};

// ═══════════════════════════════════════════════════════════════════════════
// WAVE VISUALIZER
// ═══════════════════════════════════════════════════════════════════════════
const WAVE_BARS = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█'];

function generateWave(width: number, offset: number): string {
  const bars: string[] = [];
  for (let i = 0; i < width; i++) {
    const height = Math.floor(
      4 + 3 * Math.sin((i + offset) * 0.3) + 2 * Math.cos((i + offset) * 0.5)
    );
    const barIndex = Math.max(0, Math.min(WAVE_BARS.length - 1, height));
    bars.push(WAVE_BARS[barIndex]);
  }
  return bars.join('');
}

// ═══════════════════════════════════════════════════════════════════════════
// MAIN TUI
// ═══════════════════════════════════════════════════════════════════════════
export async function runTUI(): Promise<void> {
  enableTUIMode();

  const screen = blessed.screen({
    smartCSR: true,
    title: 'LofiGirl Terminal',
    fullUnicode: true,
  });

  const stationManager = getStationManager();
  const player = getPlayer();
  const stations = stationManager.getAllStations();

  if (stations.length === 0) {
    showError(screen, 'No stations available.\nPlease add stations and try again.');
    return;
  }

  let currentStationIndex = 0;
  let waveOffset = 0;
  let lastPlayerState = PlayerState.STOPPED;
  let updateInterval: NodeJS.Timeout | null = null;

  // ╭─────────────────────────────────────────────────────────────────────╮
  // │                         LAYOUT STRUCTURE                            │
  // ╰─────────────────────────────────────────────────────────────────────╯

  // Title Bar (minimal, single line)
  const titleBar = blessed.box({
    top: 0,
    left: 0,
    width: '100%',
    height: 1,
    tags: true,
    style: {
      fg: THEME.primary,
      bg: THEME.bg,
    },
  });

  // Now Playing Box (left side, compact)
  const nowPlayingBox = blessed.box({
    top: 1,
    left: 0,
    width: '50%',
    height: 8,
    tags: true,
    border: {
      type: 'line',
    },
    style: {
      fg: THEME.fg,
      bg: THEME.bg,
      border: {
        fg: THEME.border,
      },
    },
    label: ' Now Playing ',
  });

  // Visualizer Box (right side)
  const visualizerBox = blessed.box({
    top: 1,
    left: '50%',
    width: '50%',
    height: 8,
    tags: true,
    border: {
      type: 'line',
    },
    style: {
      fg: THEME.secondary,
      bg: THEME.bg,
      border: {
        fg: THEME.border,
      },
    },
    label: ' Visualizer ',
  });

  // Station List Box
  const stationListBox = blessed.list({
    top: 9,
    left: 0,
    width: '100%',
    height: 'shrink',
    tags: true,
    border: {
      type: 'line',
    },
    style: {
      fg: THEME.fg,
      bg: THEME.bg,
      border: {
        fg: THEME.border,
      },
      selected: {
        fg: THEME.bg,
        bg: THEME.primary,
        bold: true,
      },
    },
    label: ` Stations (${currentStationIndex + 1}/${stations.length}) `,
    mouse: true,
    keys: true,
    vi: true,
    scrollbar: {
      ch: '│',
      style: {
        fg: THEME.primary,
      },
    },
  });

  // Controls Bar (bottom, minimal)
  const controlsBar = blessed.box({
    bottom: 0,
    left: 0,
    width: '100%',
    height: 1,
    tags: true,
    style: {
      fg: THEME.muted,
      bg: THEME.bg,
    },
  });

  screen.append(titleBar);
  screen.append(nowPlayingBox);
  screen.append(visualizerBox);
  screen.append(stationListBox);
  screen.append(controlsBar);

  // ╭─────────────────────────────────────────────────────────────────────╮
  // │                         UPDATE FUNCTIONS                            │
  // ╰─────────────────────────────────────────────────────────────────────╯

  function updateTitleBar(): void {
    titleBar.setContent(
      `{center}{bold}{${THEME.primary}-fg}♪ LofiGirl Terminal{/} {${THEME.muted}-fg}│ chill beats to code/relax to{/}{/bold}{/center}`
    );
  }

  function updateNowPlaying(): void {
    if (stations.length === 0) return;

    const station = stations[currentStationIndex];
    const state = player.getState();
    const volume = player.getVolume();
    const isMuted = player.isMuted();

    // State icon
    let stateIcon = '';
    let stateColor = THEME.muted;
    if (state === PlayerState.PLAYING) {
      stateIcon = '▶';
      stateColor = THEME.success;
    } else if (state === PlayerState.PAUSED) {
      stateIcon = '⏸';
      stateColor = THEME.warning;
    } else {
      stateIcon = '⏹';
      stateColor = THEME.muted;
    }

    // Volume bar (10 blocks)
    const volBars = Math.max(0, Math.min(10, Math.floor(volume / 10)));
    const volBar = '█'.repeat(volBars) + '░'.repeat(10 - volBars);
    const volDisplay = isMuted
      ? `{${THEME.error}-fg}🔇 MUTED{/}`
      : `{${THEME.secondary}-fg}${volBar}{/} {bold}${volume}%{/bold}`;

    const content = `
  {bold}{${THEME.primary}-fg}${station.name}{/}{/bold}
  {${THEME.muted}-fg}${station.genre} • ${station.description.substring(0, 40)}...{/}

  {${stateColor}-fg}${stateIcon} ${state.toUpperCase()}{/}  │  🔊 ${volDisplay}
`;

    nowPlayingBox.setContent(content);
  }

  function updateVisualizer(): void {
    const state = player.getState();

    if (state === PlayerState.PLAYING) {
      const width = (typeof visualizerBox.width === 'number' ? visualizerBox.width : 80) - 4;
      const wave1 = generateWave(width, waveOffset);
      const wave2 = generateWave(width, waveOffset + 10);
      const wave3 = generateWave(width, waveOffset + 20);

      const content = `
  {${THEME.secondary}-fg}${wave1}{/}
  {${THEME.accent}-fg}${wave2}{/}
  {${THEME.primary}-fg}${wave3}{/}

  {center}{${THEME.muted}-fg}♪ Playing... ♪{/}{/center}
`;
      visualizerBox.setContent(content);
    } else {
      const width = (typeof visualizerBox.width === 'number' ? visualizerBox.width : 80) - 4;
      const flatLine = '▁'.repeat(width);

      visualizerBox.setContent(`
  {${THEME.muted}-fg}${flatLine}{/}
  {${THEME.muted}-fg}${flatLine}{/}
  {${THEME.muted}-fg}${flatLine}{/}

  {center}{${THEME.muted}-fg}${state === PlayerState.PAUSED ? '⏸ Paused' : '⏹ Stopped'}{/}{/center}
`);
    }
  }

  function updateStationList(): void {
    const items = stations.map((station, index) => {
      const prefix = index === currentStationIndex ? '►' : ' ';
      const name = station.name.padEnd(25);
      return `{${THEME.fg}-fg}${prefix} {bold}${station.id.padEnd(20)}{/bold} ${name}{/}`;
    });

    stationListBox.setItems(items);
    stationListBox.select(currentStationIndex);
    stationListBox.setLabel(` Stations (${currentStationIndex + 1}/${stations.length}) `);
  }

  function updateControlsBar(): void {
    const controls = [
      `{${THEME.accent}-fg}[SPACE]{/} Play/Pause`,
      `{${THEME.accent}-fg}[↑↓]{/} Select`,
      `{${THEME.accent}-fg}[ENTER]{/} Play`,
      `{${THEME.accent}-fg}[M]{/} Mute`,
      `{${THEME.accent}-fg}[+/-]{/} Volume`,
      `{${THEME.error}-fg}[Q]{/} Quit`,
    ].join(' {${THEME.muted}-fg}│{/} ');

    controlsBar.setContent(` ${controls}`);
  }

  function renderAll(): void {
    updateTitleBar();
    updateNowPlaying();
    updateVisualizer();
    updateStationList();
    updateControlsBar();
    screen.render();
  }

  // ╭─────────────────────────────────────────────────────────────────────╮
  // │                         PLAYER CONTROLS                             │
  // ╰─────────────────────────────────────────────────────────────────────╯

  async function playCurrentStation(): Promise<void> {
    if (!stations || stations.length === 0) return;
    const station = stations[currentStationIndex];

    try {
      await player.loadStation(station);
      await player.play();
      renderAll();
    } catch (error) {
      // Error handling would go here
    }
  }

  async function nextStation(): Promise<void> {
    currentStationIndex = (currentStationIndex + 1) % stations.length;
    await player.stop();
    await playCurrentStation();
  }

  async function previousStation(): Promise<void> {
    currentStationIndex = (currentStationIndex - 1 + stations.length) % stations.length;
    await player.stop();
    await playCurrentStation();
  }

  // ╭─────────────────────────────────────────────────────────────────────╮
  // │                         KEYBOARD BINDINGS                           │
  // ╰─────────────────────────────────────────────────────────────────────╯

  screen.key(['space'], async () => {
    if (player.getState() === PlayerState.STOPPED) {
      await playCurrentStation();
    } else {
      await player.togglePause();
      renderAll();
    }
  });

  screen.key(['up', 'k'], () => {
    currentStationIndex = (currentStationIndex - 1 + stations.length) % stations.length;
    updateStationList();
    screen.render();
  });

  screen.key(['down', 'j'], () => {
    currentStationIndex = (currentStationIndex + 1) % stations.length;
    updateStationList();
    screen.render();
  });

  screen.key(['enter'], async () => {
    await player.stop();
    await playCurrentStation();
  });

  screen.key(['n'], async () => {
    await nextStation();
  });

  screen.key(['p'], async () => {
    await previousStation();
  });

  screen.key(['m'], async () => {
    await player.toggleMute();
    renderAll();
  });

  screen.key(['+', '='], async () => {
    await player.volumeUp(5);
    renderAll();
  });

  screen.key(['-', '_'], async () => {
    await player.volumeDown(5);
    renderAll();
  });

  screen.key(['q', 'C-c'], async () => {
    if (updateInterval) {
      clearInterval(updateInterval);
    }
    await player.stop();
    await player.cleanup();
    screen.destroy();
    disableTUIMode();
    process.exit(0);
  });

  // ╭─────────────────────────────────────────────────────────────────────╮
  // │                         ANIMATION LOOP                              │
  // ╰─────────────────────────────────────────────────────────────────────╯

  updateInterval = setInterval(() => {
    const currentState = player.getState();
    const stateChanged = currentState !== lastPlayerState;

    if (currentState === PlayerState.PLAYING) {
      waveOffset = (waveOffset + 1) % 100;
      updateVisualizer();
      screen.render();
    } else if (stateChanged) {
      updateVisualizer();
      updateNowPlaying();
      screen.render();
    }

    lastPlayerState = currentState;
  }, 100);

  // Initial render
  renderAll();
}

// ═══════════════════════════════════════════════════════════════════════════
// HELPER: ERROR DIALOG
// ═══════════════════════════════════════════════════════════════════════════
function showError(screen: blessed.Widgets.Screen, message: string): void {
  const errorBox = blessed.message({
    top: 'center',
    left: 'center',
    width: '50%',
    height: 7,
    tags: true,
    border: {
      type: 'line',
    },
    style: {
      fg: THEME.error,
      bg: THEME.bg,
      border: {
        fg: THEME.error,
      },
    },
  });

  screen.append(errorBox);
  errorBox.display(`{center}{bold}Error{/bold}\n\n${message}{/center}`, 0, () => {
    screen.destroy();
    disableTUIMode();
    process.exit(1);
  });
}
