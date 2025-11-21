"""
LofiGirl Terminal - A terminal-based lofi radio player.

This package provides a simple and elegant way to listen to lofi music
directly from your terminal.
"""

__version__ = "0.1.0"
__author__ = "LofiGirl Terminal Contributors"
__license__ = "MIT"

from lofigirl_terminal.config import Config, get_config

__all__ = ["Config", "get_config", "__version__"]
