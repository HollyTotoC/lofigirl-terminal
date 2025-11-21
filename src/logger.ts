/**
 * Logging setup for LofiGirl Terminal
 */

import winston from 'winston';
import chalk from 'chalk';
import { getConfig } from './config';

const config = getConfig();

// Global flag to disable console logging (for TUI mode)
let tuiModeEnabled = false;

// Custom log format with colors
const customFormat = winston.format.printf(({ level, message, timestamp, ...meta }) => {
  let levelColor = chalk.white;

  switch (level) {
    case 'error':
      levelColor = chalk.red;
      break;
    case 'warn':
      levelColor = chalk.yellow;
      break;
    case 'info':
      levelColor = chalk.blue;
      break;
    case 'debug':
      levelColor = chalk.gray;
      break;
  }

  const metaStr = Object.keys(meta).length ? JSON.stringify(meta) : '';
  return `${chalk.gray(timestamp)} ${levelColor(level.toUpperCase().padEnd(5))}: ${message} ${metaStr}`;
});

/**
 * Custom console transport that respects TUI mode flag dynamically
 */
class DynamicConsoleTransport extends winston.transports.Console {
  constructor(opts?: winston.transports.ConsoleTransportOptions) {
    super(opts);
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  log(info: any, callback?: () => void): void {
    // Check TUI mode flag dynamically on every log call
    if (tuiModeEnabled) {
      // Silently skip logging in TUI mode
      if (callback) callback();
      return;
    }
    // Otherwise, use normal console logging
    // @ts-ignore - Winston types are inconsistent with callback optionality
    super.log(info, callback);
  }
}

/**
 * Create and configure Winston logger
 */
export function createLogger(module: string, _tuiMode = false): winston.Logger {
  // Always create the transport, but it will check tuiModeEnabled dynamically
  const transports = [
    new DynamicConsoleTransport({
      silent: !config.debugMode && config.logLevel === 'DEBUG',
    }),
  ];

  return winston.createLogger({
    level: config.logLevel.toLowerCase(),
    format: winston.format.combine(
      winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
      winston.format.errors({ stack: true }),
      customFormat
    ),
    transports,
    defaultMeta: { module },
  });
}

export function enableTUIMode(): void {
  tuiModeEnabled = true;
}

export function disableTUIMode(): void {
  tuiModeEnabled = false;
}

export function isTUIModeEnabled(): boolean {
  return tuiModeEnabled;
}

// Default logger
export const logger = createLogger('lofigirl');
