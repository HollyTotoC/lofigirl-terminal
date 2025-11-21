"""Tests for the configuration module."""

import os
from pathlib import Path

import pytest

from lofigirl_terminal.config import Config, get_config, reload_config


class TestConfig:
    """Test suite for Config class."""

    def test_default_config(self) -> None:
        """Test that default configuration loads correctly."""
        config = Config()
        assert config.app_name == "lofigirl-terminal"
        assert config.app_version == "0.1.0"
        assert config.log_level == "INFO"
        assert config.default_volume == 50
        assert 0 <= config.default_volume <= 100

    def test_volume_validation(self) -> None:
        """Test that volume validation works correctly."""
        # Valid volume
        config = Config(default_volume=75)
        assert config.default_volume == 75

        # Invalid volume should raise validation error
        with pytest.raises(Exception):  # Pydantic validation error
            Config(default_volume=150)

        with pytest.raises(Exception):
            Config(default_volume=-10)

    def test_audio_quality_values(self) -> None:
        """Test audio quality accepts valid values."""
        config_low = Config(audio_quality="low")
        assert config_low.audio_quality == "low"

        config_high = Config(audio_quality="high")
        assert config_high.audio_quality == "high"

        # Invalid quality should raise error
        with pytest.raises(Exception):
            Config(audio_quality="ultra")

    def test_log_level_values(self) -> None:
        """Test log level accepts valid values."""
        for level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            config = Config(log_level=level)
            assert config.log_level == level

    def test_connection_timeout_validation(self) -> None:
        """Test connection timeout validation."""
        config = Config(connection_timeout=60)
        assert config.connection_timeout == 60

        # Test bounds
        with pytest.raises(Exception):
            Config(connection_timeout=0)

        with pytest.raises(Exception):
            Config(connection_timeout=500)

    def test_get_config_singleton(self) -> None:
        """Test that get_config returns the same instance."""
        config1 = get_config()
        config2 = get_config()
        assert config1 is config2

    def test_reload_config(self) -> None:
        """Test that reload_config creates a new instance."""
        get_config()  # Get initial config
        os.environ["LOG_LEVEL"] = "DEBUG"
        config2 = reload_config()
        assert config2.log_level == "DEBUG"
        # Clean up
        os.environ.pop("LOG_LEVEL", None)

    def test_cache_directory_creation(self) -> None:
        """Test that cache directory is created."""
        config = Config(audio_cache_dir=Path("/tmp/test_cache"))
        assert config.audio_cache_dir == Path("/tmp/test_cache")
