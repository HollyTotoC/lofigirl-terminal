#!/usr/bin/env node

/**
 * LofiGirl Terminal - Entry Point
 *
 * A cross-platform terminal-based lofi radio player
 * Supports PowerShell (Windows), Terminal (Mac/Linux)
 */

import { runCLI } from './cli';
import { logger } from './logger';
import { initializeApp } from './startup';

async function main(): Promise<void> {
  try {
    // Initialize application (scan YouTube streams, setup stations)
    await initializeApp();

    // Run CLI
    await runCLI();
  } catch (error) {
    logger.error(`Fatal error: ${error}`);
    process.exit(1);
  }
}

// Handle uncaught errors
process.on('uncaughtException', (error) => {
  logger.error(`Uncaught exception: ${error}`);
  process.exit(1);
});

process.on('unhandledRejection', (reason) => {
  logger.error(`Unhandled rejection: ${reason}`);
  process.exit(1);
});

main();
