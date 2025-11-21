"""
Configuration management for LofiGirl Terminal.

This module handles loading and validating configuration from environment
variables and .env files using Pydantic for type safety and validation.
"""

from pathlib import Path
from typing import Literal, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
    Application configuration with validation.

    This class defines all configuration options for the application,
    loads them from environment variables, and validates them.

    Attributes:
        app_name: Name of the application
        app_version: Version of the application
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        default_volume: Default volume level (0-100)
        audio_quality: Audio quality setting
        audio_cache_enabled: Whether to enable audio caching
        audio_cache_dir: Directory for audio cache
        connection_timeout: Connection timeout in seconds
        retry_attempts: Number of retry attempts for network requests
        stream_buffer_size: Size of streaming buffer
        theme: UI theme
        show_visualizer: Whether to show audio visualizer
        update_interval: UI update interval in seconds
        default_station: Default radio station
        debug_mode: Enable debug mode
        enable_profiling: Enable performance profiling
    """

    model_config = SettingsConfigDict(
        env_file=[
            ".env",
            str(Path.home() / ".config" / "lofigirl-terminal" / "config.env"),
        ],
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application Settings
    app_name: str = Field(
        default="lofigirl-terminal",
        description="Name of the application",
    )
    app_version: str = Field(
        default="0.1.0",
        description="Version of the application",
    )
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level",
    )

    # Audio Settings
    default_volume: int = Field(
        default=50,
        ge=0,
        le=100,
        description="Default volume level (0-100)",
    )
    audio_quality: Literal["low", "medium", "high"] = Field(
        default="high",
        description="Audio quality setting",
    )
    audio_cache_enabled: bool = Field(
        default=False,
        description="Enable audio caching",
    )
    audio_cache_dir: Path = Field(
        default=Path(".cache/audio"),
        description="Directory for audio cache",
    )

    # Network Settings
    connection_timeout: int = Field(
        default=30,
        ge=1,
        le=300,
        description="Connection timeout in seconds",
    )
    retry_attempts: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Number of retry attempts",
    )
    stream_buffer_size: int = Field(
        default=4096,
        ge=1024,
        le=65536,
        description="Stream buffer size in bytes",
    )

    # UI Settings
    theme: str = Field(
        default="catppuccin-mocha",
        description="UI color theme (catppuccin-mocha, dracula, nord, tokyo-night, etc.)",
    )
    terminal_font: Optional[str] = Field(
        default=None,
        description="Terminal font name (e.g., 'JetBrainsMono Nerd Font')",
    )
    ascii_art: str = Field(
        default="lofi-girl-classic",
        description="ASCII art ID (lofi-girl-classic, music-notes, vinyl-record, etc.)",
    )
    show_visualizer: bool = Field(
        default=True,
        description="Show audio visualizer",
    )
    update_interval: int = Field(
        default=1,
        ge=1,
        le=10,
        description="UI update interval in seconds",
    )

    # Station Settings
    default_station: str = Field(
        default="lofi-hip-hop",
        description="Default radio station",
    )

    # Development Settings
    debug_mode: bool = Field(
        default=False,
        description="Enable debug mode",
    )
    enable_profiling: bool = Field(
        default=False,
        description="Enable performance profiling",
    )

    @field_validator("audio_cache_dir")
    @classmethod
    def create_cache_dir(cls, v: Path) -> Path:
        """
        Ensure cache directory exists if caching is enabled.

        Args:
            v: The cache directory path

        Returns:
            The validated cache directory path
        """
        if not v.exists():
            v.mkdir(parents=True, exist_ok=True)
        return v


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get the global configuration instance.

    This function implements a singleton pattern to ensure only one
    configuration instance exists throughout the application lifecycle.

    Returns:
        The global Config instance

    Example:
        >>> config = get_config()
        >>> print(config.app_name)
        lofigirl-terminal
    """
    global _config
    if _config is None:
        _config = Config()
    return _config


def reload_config() -> Config:
    """
    Reload the configuration from environment.

    This function forces a reload of the configuration, useful for
    testing or when environment variables change.

    Returns:
        A fresh Config instance

    Example:
        >>> os.environ['LOG_LEVEL'] = 'DEBUG'
        >>> config = reload_config()
        >>> print(config.log_level)
        DEBUG
    """
    global _config
    _config = Config()
    return _config
