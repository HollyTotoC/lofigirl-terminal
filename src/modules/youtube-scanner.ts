/**
 * YouTube Live Stream Scanner
 * Scans YouTube channels for live streams and converts them to Station objects
 */

import axios from 'axios';
import * as cheerio from 'cheerio';
import { Station } from '../types';
import { createLogger } from '../logger';

const logger = createLogger('youtube-scanner');

const LOFIGIRL_CHANNEL_URL = 'https://www.youtube.com/@LofiGirl/streams';
const LOFIGIRL_CHANNEL_ID = 'UCSJ4gkVC6NrvII8umztf0Ow'; // @LofiGirl channel ID

interface YouTubeVideo {
  videoId: string;
  title: string;
  isLive: boolean;
  thumbnail?: string;
}

/**
 * Scan for live streams using YouTube Data API v3
 */
async function scanWithAPI(apiKey: string): Promise<YouTubeVideo[]> {
  try {
    logger.info('Scanning for live streams using YouTube API...');

    const response = await axios.get('https://www.googleapis.com/youtube/v3/search', {
      params: {
        part: 'snippet',
        channelId: LOFIGIRL_CHANNEL_ID,
        eventType: 'live',
        type: 'video',
        key: apiKey,
        maxResults: 10,
      },
    });

    const videos: YouTubeVideo[] = response.data.items.map((item: any) => ({
      videoId: item.id.videoId,
      title: item.snippet.title,
      isLive: item.snippet.liveBroadcastContent === 'live',
      thumbnail: item.snippet.thumbnails?.high?.url,
    }));

    logger.info(`Found ${videos.length} live streams via API`);
    return videos;
  } catch (error: any) {
    logger.error('Failed to scan with YouTube API:', error.message);
    throw error;
  }
}

/**
 * Scan for live streams using YouTube RSS feed (no API key needed, no scraping)
 */
async function scanWithRSSFeed(): Promise<YouTubeVideo[]> {
  try {
    logger.info('Scanning for live streams using YouTube RSS feed...');

    const rssUrl = `https://www.youtube.com/feeds/videos.xml?channel_id=${LOFIGIRL_CHANNEL_ID}`;
    const response = await axios.get(rssUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      },
    });

    const xml = response.data;

    // Parse XML to extract video IDs and titles
    // Simple regex parsing (could use xml2js for production)
    const videoRegex = /<entry>[\s\S]*?<yt:videoId>(.*?)<\/yt:videoId>[\s\S]*?<title>(.*?)<\/title>[\s\S]*?<\/entry>/g;
    const videos: YouTubeVideo[] = [];

    let match;
    while ((match = videoRegex.exec(xml)) !== null) {
      videos.push({
        videoId: match[1],
        title: match[2],
        isLive: false, // RSS doesn't indicate live status, we'll check later
      });

      // Limit to first 10 videos
      if (videos.length >= 10) break;
    }

    logger.info(`Found ${videos.length} recent videos from RSS feed`);
    return videos;
  } catch (error: any) {
    logger.error(`Failed to scan with RSS feed: ${error.message}`);
    throw error;
  }
}

/**
 * Scan for live streams by scraping the YouTube page HTML
 */
async function scanWithWebScraping(): Promise<YouTubeVideo[]> {
  try {
    logger.info('Scanning for live streams using web scraping...');

    const response = await axios.get(LOFIGIRL_CHANNEL_URL, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
      },
    });

    const html = response.data;

    // Extract ytInitialData from the page
    const ytInitialDataMatch = html.match(/var ytInitialData = ({.*?});/);
    if (!ytInitialDataMatch) {
      logger.warn('Could not find ytInitialData in page HTML');
      return [];
    }

    const ytInitialData = JSON.parse(ytInitialDataMatch[1]);

    // Navigate the complex YouTube data structure
    const tabs = ytInitialData?.contents?.twoColumnBrowseResultsRenderer?.tabs || [];
    let videoItems: any[] = [];

    for (const tab of tabs) {
      const tabRenderer = tab.tabRenderer;
      if (tabRenderer?.content?.richGridRenderer) {
        const contents = tabRenderer.content.richGridRenderer.contents || [];
        videoItems = contents
          .filter((item: any) => item.richItemRenderer?.content?.videoRenderer)
          .map((item: any) => item.richItemRenderer.content.videoRenderer);
        break;
      }
    }

    // Extract live streams
    const videos: YouTubeVideo[] = videoItems
      .filter((video: any) => {
        // Check if it's a live stream
        const badges = video.badges || [];
        return badges.some((badge: any) =>
          badge.metadataBadgeRenderer?.style === 'BADGE_STYLE_TYPE_LIVE_NOW' ||
          badge.metadataBadgeRenderer?.label === 'LIVE'
        );
      })
      .map((video: any) => ({
        videoId: video.videoId,
        title: video.title?.runs?.[0]?.text || 'Unknown',
        isLive: true,
        thumbnail: video.thumbnail?.thumbnails?.[0]?.url,
      }));

    logger.info(`Found ${videos.length} live streams via web scraping`);
    return videos;
  } catch (error: any) {
    logger.error(`Failed to scan with web scraping: ${error.message}`);
    if (error.response) {
      logger.error(`HTTP Status: ${error.response.status}`);
    }
    throw error;
  }
}

/**
 * Convert YouTube video to Station object
 */
function videoToStation(video: YouTubeVideo, index: number): Station {
  // Generate a genre based on the title keywords
  let genre = 'lofi';
  const titleLower = video.title.toLowerCase();

  if (titleLower.includes('hip hop') || titleLower.includes('beats')) {
    genre = 'lofi-hip-hop';
  } else if (titleLower.includes('jazz')) {
    genre = 'lofi-jazz';
  } else if (titleLower.includes('sleep') || titleLower.includes('calm')) {
    genre = 'lofi-sleep';
  } else if (titleLower.includes('study') || titleLower.includes('focus')) {
    genre = 'lofi-study';
  }

  return {
    id: `lofi-live-${index + 1}`,
    name: video.title,
    url: `https://www.youtube.com/watch?v=${video.videoId}`,
    description: `🔴 LIVE: ${video.title}`,
    genre,
  };
}

/**
 * Scan Lofi Girl channel for live streams
 * @param apiKey - Optional YouTube API key. If provided, uses API. Otherwise uses web scraping.
 * @returns Array of Station objects representing live streams
 */
export async function scanLofiGirlLiveStreams(apiKey?: string): Promise<Station[]> {
  try {
    logger.info('Starting YouTube stream scan for @LofiGirl...');

    let videos: YouTubeVideo[] = [];

    // Try API first if key is provided
    if (apiKey) {
      try {
        videos = await scanWithAPI(apiKey);
      } catch (error) {
        logger.warn('API scan failed, falling back to RSS feed');
        try {
          videos = await scanWithRSSFeed();
        } catch (rssError) {
          logger.warn('RSS feed failed, falling back to web scraping');
          videos = await scanWithWebScraping();
        }
      }
    } else {
      // Use RSS feed first (most reliable, no API key needed)
      try {
        videos = await scanWithRSSFeed();
      } catch (error) {
        logger.warn('RSS feed failed, falling back to web scraping');
        videos = await scanWithWebScraping();
      }
    }

    // For API results, filter to only live streams
    // For RSS/scraping results, take all recent videos (since RSS doesn't indicate live status reliably)
    const relevantVideos = apiKey
      ? videos.filter(v => v.isLive)
      : videos; // Take all recent videos from RSS

    if (relevantVideos.length === 0) {
      logger.warn('No videos found on @LofiGirl channel');
      return [];
    }

    // Convert to Station objects
    const stations = relevantVideos.map((video, index) => videoToStation(video, index));

    logger.info(`Successfully scanned ${stations.length} streams from @LofiGirl`);
    return stations;
  } catch (error: any) {
    logger.error(`Failed to scan streams: ${error.message}`);
    throw error;
  }
}

/**
 * Scan with fallback: tries both methods and returns first successful result
 */
export async function scanLofiGirlLiveStreamsWithFallback(apiKey?: string): Promise<Station[]> {
  try {
    return await scanLofiGirlLiveStreams(apiKey);
  } catch (error) {
    logger.error('All scan methods failed');
    return [];
  }
}
