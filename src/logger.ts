/**
 * Logging setup for LofiGirl Terminal
 */

import winston from 'winston';
import chalk from 'chalk';
import { getConfig } from './config';

const config = getConfig();

// Custom log format with colors
const customFormat = winston.format.printf(
  ({ level, message, timestamp, ...meta }) => {
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
  }
);

/**
 * Create and configure Winston logger
 */
export function createLogger(module: string): winston.Logger {
  return winston.createLogger({
    level: config.logLevel.toLowerCase(),
    format: winston.format.combine(
      winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
      winston.format.errors({ stack: true }),
      customFormat
    ),
    transports: [
      new winston.transports.Console({
        silent: !config.debugMode && config.logLevel === 'DEBUG',
      }),
    ],
    defaultMeta: { module },
  });
}

// Default logger
export const logger = createLogger('lofigirl');
