/**
 * Dependency checking utilities
 */

import { execFileSync } from 'child_process';
import { createLogger } from '../logger';

const logger = createLogger('dependencies');

/**
 * Check if a command is available in PATH
 */
export function isCommandAvailable(command: string): boolean {
  try {
    if (process.platform === 'win32') {
      execFileSync('where', [command], { stdio: 'ignore' });
    } else {
      execFileSync('which', [command], { stdio: 'ignore' });
    }
    return true;
  } catch {
    return false;
  }
}

/**
 * Check if yt-dlp or youtube-dl is available
 */
export function checkYouTubeExtractor(): {
  available: boolean;
  extractor: string | null;
} {
  if (isCommandAvailable('yt-dlp')) {
    logger.debug('Found yt-dlp');
    return { available: true, extractor: 'yt-dlp' };
  } else if (isCommandAvailable('youtube-dl')) {
    logger.debug('Found youtube-dl');
    return { available: true, extractor: 'youtube-dl' };
  } else {
    logger.warn('Neither yt-dlp nor youtube-dl found in PATH');
    return { available: false, extractor: null };
  }
}

/**
 * Check if MPV is available
 */
export function checkMPV(): boolean {
  const available = isCommandAvailable('mpv');
  if (available) {
    logger.debug('Found mpv');
  } else {
    logger.warn('mpv not found in PATH');
  }
  return available;
}

/**
 * Get installation instructions for missing dependencies
 */
export function getInstallInstructions(): string {
  const ytCheck = checkYouTubeExtractor();
  const mpvCheck = checkMPV();

  if (ytCheck.available && mpvCheck) {
    return 'All dependencies are installed!';
  }

  let instructions = '\n⚠️  Missing Dependencies:\n\n';

  if (!mpvCheck) {
    instructions += '❌ MPV media player not found\n';
    if (process.platform === 'win32') {
      instructions += '   Install: choco install mpv\n';
      instructions += '   Or download: https://mpv.io/installation/\n\n';
    } else if (process.platform === 'darwin') {
      instructions += '   Install: brew install mpv\n\n';
    } else {
      instructions += '   Install: sudo apt install mpv (Debian/Ubuntu)\n';
      instructions += '           sudo dnf install mpv (Fedora)\n\n';
    }
  }

  if (!ytCheck.available) {
    instructions += '❌ yt-dlp/youtube-dl not found (required for YouTube streaming)\n';
    if (process.platform === 'win32') {
      instructions += '   Install: choco install yt-dlp\n';
      instructions += '   Or: pip install yt-dlp\n';
      instructions += '   Or download: https://github.com/yt-dlp/yt-dlp/releases\n\n';
    } else if (process.platform === 'darwin') {
      instructions += '   Install: brew install yt-dlp\n';
      instructions += '   Or: pip install yt-dlp\n\n';
    } else {
      instructions += '   Install: pip install yt-dlp\n';
      instructions += '   Or: sudo apt install yt-dlp (Debian/Ubuntu)\n\n';
    }
  }

  instructions +=
    '📖 For more information, visit: https://github.com/HollyTotoC/lofigirl-terminal#installation';

  return instructions;
}
