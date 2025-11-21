# 🎵 LofiGirl Terminal

<div align="center">

[![CI](https://github.com/HollyTotoC/lofigirl-terminal/workflows/CI/badge.svg)](https://github.com/HollyTotoC/lofigirl-terminal/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A beautiful terminal-based lofi radio player. Bring relaxing lofi beats to your command line! 🎧

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Development](#-development) • [Contributing](#-contributing)

</div>

---

## 📖 About

**LofiGirl Terminal** is a terminal application inspired by the popular "lofi girl" YouTube streams. It brings the calming vibes of lofi music directly to your terminal, perfect for coding, studying, or just relaxing.

### ✨ Features

- 🎧 **Multiple Stations**: Choose from various lofi radio stations
- 🎨 **Beautiful UI**: Clean and minimalist terminal interface using Rich
- ⚙️ **Configurable**: Customize volume, quality, and other settings
- 🔌 **Extensible**: Easy to add custom stations
- 🧪 **Well Tested**: Comprehensive test suite with high coverage
- 📦 **Easy Setup**: Simple installation and configuration
- 🚀 **Cross-platform**: Works on Linux, macOS, and Windows

### 🔮 Planned Features

- Interactive TUI with playback controls
- Audio visualizations
- Favorites/playlist system
- Local music file support
- Pomodoro timer integration
- Multiple themes

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/HollyTotoC/lofigirl-terminal.git
cd lofigirl-terminal

# Install using make (recommended)
make setup

# Or manually:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements/dev.txt
pip install -e .
```

### Install from PyPI (Coming Soon)

```bash
pip install lofigirl-terminal
```

## 📚 Usage

### Basic Commands

```bash
# Show help
lofigirl --help

# List available stations
lofigirl list

# Play default station
lofigirl play

# Play specific station
lofigirl play --station lofi-jazz

# Play with custom volume
lofigirl play --volume 75

# Show application info
lofigirl info

# Get station details
lofigirl station-info --station lofi-hip-hop
```

### Available Stations

- **lofi-hip-hop**: 24/7 chill lofi hip hop beats to study/relax to
- **lofi-jazz**: Smooth jazz with lofi aesthetics
- **lofi-sleep**: Calming lofi beats for sleep and meditation
- **lofi-study**: Focus-enhancing lofi beats for studying

### Configuration

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Available configuration options:

```env
# Application Settings
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR, CRITICAL
DEFAULT_VOLUME=50           # 0-100
AUDIO_QUALITY=high          # low, medium, high
DEFAULT_STATION=lofi-hip-hop

# UI Settings
THEME=default               # default, dark, light
SHOW_VISUALIZER=true
UPDATE_INTERVAL=1           # seconds
```

## 🛠️ Development

### Setup Development Environment

```bash
# Complete setup (creates venv, installs deps, sets up pre-commit)
make setup

# Or step by step:
make venv              # Create virtual environment
make install-dev       # Install dependencies
make pre-commit-install # Set up git hooks
```

### Development Commands

```bash
# Run tests
make test              # Run tests with coverage
make test-fast         # Run tests without coverage
make test-watch        # Run tests in watch mode

# Code quality
make format            # Format code with black & isort
make lint              # Run flake8 linter
make type-check        # Run mypy type checker
make check-all         # Run all checks

# Run the application
make run               # Show help
make run-play          # Play default station
make run-list          # List stations

# Utilities
make clean             # Clean temporary files
make clean-all         # Clean everything including venv
```

### Project Structure

```
lofigirl-terminal/
├── src/
│   └── lofigirl_terminal/      # Main package
│       ├── __init__.py
│       ├── main.py             # CLI entry point
│       ├── config.py           # Configuration management
│       ├── logger.py           # Logging setup
│       └── modules/
│           ├── stations.py     # Station management
│           └── player.py       # Audio player
├── tests/                      # Test suite
│   ├── test_config.py
│   ├── test_stations.py
│   └── test_player.py
├── requirements/               # Dependencies
│   ├── base.txt               # Production dependencies
│   ├── dev.txt                # Development dependencies
│   └── prod.txt               # Production-only dependencies
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI
├── docs/                      # Documentation
├── .gitignore
├── .env.example               # Example configuration
├── pyproject.toml             # Project metadata & config
├── setup.py                   # Setup script
├── Makefile                   # Development commands
├── CLAUDE.md                  # Project tracker
└── README.md                  # This file
```

### Adding a New Station

```python
from lofigirl_terminal.modules.stations import Station, StationManager

# Create a custom station
custom_station = Station(
    id="my-station",
    name="My Custom Station",
    url="https://example.com/stream-url",
    description="Description of the station",
    genre="lofi"
)

# Add to manager
manager = StationManager()
manager.add_station(custom_station)
```

### Running Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=lofigirl_terminal

# Run specific test file
pytest tests/test_stations.py -v

# Run with specific Python version
python3.11 -m pytest tests/ -v
```

## 🤝 Contributing

We welcome contributions from the community! Whether it's:

- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🎨 UI/UX enhancements
- 🧪 Additional tests

Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a PR.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `make test`
5. Run quality checks: `make check-all`
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Code Standards

- **Code Style**: Black formatter (88 char line length)
- **Linting**: Flake8 with Google-style docstrings
- **Type Hints**: Full type annotations for all functions
- **Testing**: Minimum 80% code coverage
- **Commits**: Conventional commits format

## 📋 Roadmap

- [x] Project structure and setup
- [x] Basic CLI interface
- [x] Station management
- [x] Configuration system
- [x] Test suite
- [x] CI/CD pipeline
- [ ] Implement actual audio streaming
- [ ] Interactive TUI interface
- [ ] Audio visualizations
- [ ] Playlist/favorites system
- [ ] PyPI package distribution
- [ ] Plugin system
- [ ] Documentation website

See [CLAUDE.md](CLAUDE.md) for detailed development tracking.

## 🐛 Known Issues

- Audio playback is currently a mock implementation (needs audio library integration)
- Streaming URLs are placeholders and need to be replaced with actual sources
- TUI interface is planned but not yet implemented

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the [Lofi Girl](https://www.youtube.com/c/LofiGirl) YouTube channel
- Built with [Click](https://click.palletsprojects.com/) for CLI
- UI powered by [Rich](https://rich.readthedocs.io/)
- Configuration using [Pydantic](https://pydantic-docs.helpmanual.io/)

## 📞 Support & Community

- **Issues**: [GitHub Issues](https://github.com/HollyTotoC/lofigirl-terminal/issues)
- **Discussions**: [GitHub Discussions](https://github.com/HollyTotoC/lofigirl-terminal/discussions)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

<div align="center">

**Made with ❤️ by the community**

[Report Bug](https://github.com/HollyTotoC/lofigirl-terminal/issues) • [Request Feature](https://github.com/HollyTotoC/lofigirl-terminal/issues) • [Documentation](./docs/)

</div>
