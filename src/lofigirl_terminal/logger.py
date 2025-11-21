"""
Logging configuration for LofiGirl Terminal.

This module sets up colored logging with appropriate formatting for
both console output and file logging.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

import colorlog

from lofigirl_terminal.config import get_config


def setup_logger(
    name: str = "lofigirl_terminal",
    log_file: Optional[Path] = None,
) -> logging.Logger:
    """
    Set up a logger with colored console output and optional file logging.

    Args:
        name: Name of the logger
        log_file: Optional path to log file. If None, only console logging is used.

    Returns:
        Configured logger instance

    Example:
        >>> logger = setup_logger("my_module")
        >>> logger.info("Application started")
        >>> logger.error("Something went wrong")
    """
    config = get_config()

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.log_level))

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Console handler with colors
    console_handler = colorlog.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, config.log_level))

    # Colored formatter for console
    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(name)s%(reset)s: %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Simple formatter for file
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger with the given name.

    This is a convenience function that returns an existing logger or
    creates a new one with default settings.

    Args:
        name: Name of the logger, typically __name__ of the module

    Returns:
        Logger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.debug("Debug message")
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger
