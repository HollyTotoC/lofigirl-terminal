/**
 * Configuration management for LofiGirl Terminal
 */

import * as dotenv from 'dotenv';
import { z } from 'zod';
import { AppConfig } from './types';

// Load .env file
dotenv.config();

// Configuration schema with validation
const ConfigSchema = z.object({
  appName: z.string().default('LofiGirl Terminal'),
  logLevel: z.enum(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']).default('INFO'),
  defaultVolume: z.number().min(0).max(100).default(50),
  audioQuality: z.enum(['low', 'medium', 'high']).default('high'),
  defaultStation: z.string().default('lofi-hip-hop'),
  theme: z.string().default('default'),
  debugMode: z.boolean().default(false),
  showVisualizer: z.boolean().default(true),
  updateInterval: z.number().default(1),
  youtubeApiKey: z.string().optional(),
});

/**
 * Get application configuration from environment variables
 */
export function getConfig(): AppConfig {
  const config = {
    appName: process.env.APP_NAME || 'LofiGirl Terminal',
    logLevel: process.env.LOG_LEVEL || 'INFO',
    defaultVolume: parseInt(process.env.DEFAULT_VOLUME || '50', 10),
    audioQuality: process.env.AUDIO_QUALITY || 'high',
    defaultStation: process.env.DEFAULT_STATION || 'lofi-hip-hop',
    theme: process.env.THEME || 'default',
    debugMode: process.env.DEBUG_MODE === 'true',
    showVisualizer: process.env.SHOW_VISUALIZER !== 'false',
    updateInterval: parseInt(process.env.UPDATE_INTERVAL || '1', 10),
    youtubeApiKey: process.env.YOUTUBE_API_KEY,
  };

  // Validate and return
  return ConfigSchema.parse(config);
}
