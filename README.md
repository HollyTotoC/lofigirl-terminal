# 🎵 LofiGirl Terminal

<div align="center">

[![CI](https://github.com/HollyTotoC/lofigirl-terminal/workflows/CI/badge.svg)](https://github.com/HollyTotoC/lofigirl-terminal/actions)
[![Node.js 16+](https://img.shields.io/badge/node-%3E%3D16.0.0-brightgreen.svg)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue.svg)](https://www.typescriptlang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Cross-Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/HollyTotoC/lofigirl-terminal)

**Cross-platform terminal-based lofi radio player**
Native support for PowerShell (Windows), Terminal (Mac/Linux)! 🎧

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Migration](#-migration-from-python) • [Contributing](#-contributing)

</div>

---

## 🆕 Major Update: Now in Node.js/TypeScript!

**LofiGirl Terminal** has been migrated from Python to **Node.js/TypeScript** for superior cross-platform compatibility!

### Why the Change?

- ✅ **True Cross-Platform**: npm works identically on Windows, Mac, Linux
- ✅ **Native PowerShell**: First-class Windows PowerShell support
- ✅ **Simpler Setup**: No virtual environments, no PATH issues
- ✅ **Universal Install**: `npm install -g` works everywhere
- ✅ **Better DX**: TypeScript with full type safety

> **Coming from Python version?** See [Migration Guide](#-migration-from-python) below.

---

## 📖 About

**LofiGirl Terminal** is a terminal application inspired by the popular "lofi girl" YouTube streams. It brings the calming vibes of lofi music directly to your terminal, perfect for coding, studying, or just relaxing.

### ✨ Features

#### 🎵 Audio Streaming
- 🎧 **Real YouTube Streaming**: Direct integration with official LofiGirl channels
- 📻 **Multiple Stations**: 4 curated lofi stations (hip-hop, sleep, jazz, study)
- 🎛️ **Full Playback Control**: Play, pause, stop, next/previous
- 🔊 **Volume Management**: Volume control, mute, adjustable levels

#### 🎨 Interactive TUI
- 🖼️ **Blessed TUI**: Cross-platform terminal interface
- 📊 **Real-time Status**: Live playback status and volume display
- ⌨️ **Keyboard Shortcuts**: Complete keyboard control (SPACE, N, P, M, +/-, Q)
- 🎨 **Colorful Display**: Rich colors with chalk and boxen
- 🖱️ **Mouse Support**: Clickable buttons for all actions

#### 🛠️ Technical
- ⚡ **TypeScript**: Fully typed for better development experience
- 🌍 **Cross-platform**: Works on Windows, Mac, Linux natively
- 📦 **npm Package**: Easy global installation
- 🔌 **MPV Backend**: Professional audio playback
- ⚙️ **Configurable**: Customize via .env file

### 🔮 Planned Features

- 💾 Favorites/playlist system
- 🎵 Local music file support
- ⏲️ Pomodoro timer integration
- 🎨 Advanced visualizations
- 🎥 Video mode support

---

## 🚀 Installation

### Prerequisites

- **Node.js 16+** (LTS recommended) - [Download](https://nodejs.org/)
- **npm** (comes with Node.js)
- **MPV media player** (for audio playback) - [Download](https://mpv.io/installation/)
- **yt-dlp** or **youtube-dl** (for YouTube streaming) - [Download](https://github.com/yt-dlp/yt-dlp)
- **Git**

> **Note**: yt-dlp is required for playing YouTube streams. Without it, YouTube URLs won't work.

### 🪟 Windows (PowerShell)

Install with a single PowerShell command:

```powershell
irm https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install-node.ps1 | iex
```

This will:
- ✅ Check Node.js installation
- ✅ Check/install MPV (via Chocolatey)
- ✅ Clone repository
- ✅ Install npm dependencies
- ✅ Build TypeScript
- ✅ Create launcher in PATH

**Install yt-dlp for YouTube streaming:**
```powershell
choco install yt-dlp
# OR
pip install yt-dlp
```

**Then simply run:**
```powershell
lofigirl tui
```

### 🍎 macOS / 🐧 Linux

Install with a single bash command:

```bash
curl -sSL https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install-node.sh | bash
```

This will:
- ✅ Check Node.js installation
- ✅ Check/install MPV (via package manager)
- ✅ Clone repository to `~/.lofigirl-terminal`
- ✅ Install npm dependencies
- ✅ Build TypeScript
- ✅ Create launcher at `~/.local/bin/lofigirl`

**Install yt-dlp for YouTube streaming:**
```bash
# macOS
brew install yt-dlp

# Ubuntu/Debian
sudo apt install yt-dlp
# OR
pip install yt-dlp

# Fedora
sudo dnf install yt-dlp
```

**Then simply run:**
```bash
lofigirl tui
```

### 📦 Manual Installation

```bash
# Clone the repository
git clone https://github.com/HollyTotoC/lofigirl-terminal.git
cd lofigirl-terminal

# Install dependencies
npm install

# Install yt-dlp (if not already installed)
pip install yt-dlp

# Build TypeScript
npm run build

# Run
node dist/index.js tui
```

### ✅ Verify Installation

Check if all dependencies are installed:
```bash
lofigirl check
```

This will show you which dependencies are installed and provide installation instructions for any missing ones.

### 🗑️ Uninstall

To completely remove LofiGirl Terminal:

**Windows:**
```powershell
Remove-Item $env:USERPROFILE\lofigirl-terminal -Recurse
```

**Mac/Linux:**
```bash
rm -rf ~/.lofigirl-terminal ~/.local/bin/lofigirl
```

---

## 📚 Usage

### 🎨 Interactive TUI (Recommended)

Launch the beautiful Terminal User Interface:

```bash
lofigirl tui
```

**Keyboard Controls:**
- `SPACE` - Play/Pause
- `N` - Next station
- `P` - Previous station
- `M` - Mute/Unmute
- `+` or `=` - Volume up
- `-` or `_` - Volume down
- `Q` or `Ctrl+C` - Quit

### 📟 CLI Commands

```bash
# Show help
lofigirl --help

# Launch interactive TUI
lofigirl tui

# List available stations
lofigirl list

# Play default station (CLI mode)
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

Create a `.env` file in the installation directory:

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

---

## 🔄 Migration from Python

### For Users

If you have the **Python version** installed:

1. **Uninstall Python version:**
   ```bash
   # Linux/Mac
   bash ~/.lofigirl-terminal/uninstall.sh

   # Windows PowerShell
   Remove-Item $env:USERPROFILE\lofigirl-terminal -Recurse
   ```

2. **Install Node.js version:**
   ```bash
   # Use the installation commands above
   ```

3. **Done!** All your preferences are preserved.

### For Developers

See detailed migration guide: [MIGRATION.md](MIGRATION.md)

### Why Migrate?

| Python Version | Node.js Version |
|----------------|-----------------|
| Complex venv setup | Simple npm install |
| Platform-specific issues | Universal compatibility |
| Windows PATH problems | Native PowerShell support |
| 5-7 installation steps | 2 installation steps |
| libmpv-2.dll issues | Clean MPV integration |

**Full comparison:** [MIGRATION.md](MIGRATION.md)

---

## 🛠️ Development

### Quick Start

```bash
# Clone repository
git clone https://github.com/HollyTotoC/lofigirl-terminal.git
cd lofigirl-terminal

# Install dependencies
npm install

# Build TypeScript
npm run build

# Run in development mode
npm run dev
```

### Development Commands

```bash
# Build TypeScript
npm run build

# Watch mode (auto-rebuild)
npm run build:watch

# Run in development
npm run dev

# Lint code
npm run lint

# Format code
npm run format

# Run tests
npm test

# Clean build
npm run clean
```

### Project Structure

```
lofigirl-terminal/
├── src/                      # TypeScript source
│   ├── index.ts             # Entry point
│   ├── cli.ts               # CLI commands (Commander.js)
│   ├── config.ts            # Configuration (Zod)
│   ├── logger.ts            # Logging (Winston)
│   ├── types.ts             # TypeScript types
│   └── modules/
│       ├── stations.ts      # Station management
│       ├── player.ts        # MPV player wrapper
│       └── tui.ts           # TUI interface (blessed)
├── dist/                    # Compiled JavaScript
├── package.json             # npm configuration
├── tsconfig.json            # TypeScript config
└── README.md                # This file
```

### Technology Stack

| Component | Library |
|-----------|---------|
| Language | TypeScript 5.3 |
| CLI Framework | Commander.js |
| TUI | Blessed |
| Terminal Colors | Chalk |
| Audio Player | node-mpv |
| Configuration | Zod + dotenv |
| Logging | Winston |
| Testing | Jest |

---

## 🤝 Contributing

We welcome contributions! Whether it's:

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
4. Run tests: `npm test`
5. Run quality checks: `npm run lint && npm run format`
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Code Standards

- **Code Style**: Prettier (automatic formatting)
- **Linting**: ESLint with TypeScript support
- **Type Safety**: Full TypeScript type annotations
- **Testing**: Jest with coverage
- **Commits**: Conventional commits format

---

## 📋 Roadmap

### ✅ Completed
- [x] Project structure and setup
- [x] TypeScript migration complete
- [x] CLI interface with all commands
- [x] TUI interface with blessed
- [x] Configuration system
- [x] Station management (4 stations)
- [x] MPV player integration
- [x] Cross-platform installers (PowerShell + Bash)
- [x] Full documentation

### 🚧 In Progress
- [ ] YouTube streaming integration (ytdl-core)
- [ ] Advanced audio visualizations
- [ ] npm package publication

### 📅 Planned
- [ ] Playlist/favorites system
- [ ] Local music file support
- [ ] Pomodoro timer integration
- [ ] Windows Store package
- [ ] Homebrew formula (Mac)
- [ ] APT/YUM packages (Linux)
- [ ] Plugin system
- [ ] CI/CD pipeline

---

## 📚 Documentation

- **Quick Start**: [QUICKSTART-NODE.md](QUICKSTART-NODE.md)
- **Migration Guide**: [MIGRATION.md](MIGRATION.md)
- **Migration Summary**: [MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)
- **Project Tracker**: [CLAUDE.md](CLAUDE.md)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🐛 Known Issues

- MPV must be installed separately (auto-install coming soon)
- Some YouTube URLs may require periodic updates
- Video mode requires terminal with sixel/kitty graphics support

**Report issues:** [GitHub Issues](https://github.com/HollyTotoC/lofigirl-terminal/issues)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by the [Lofi Girl](https://www.youtube.com/c/LofiGirl) YouTube channel
- Built with:
  - [Commander.js](https://github.com/tj/commander.js/) - CLI framework
  - [Blessed](https://github.com/chjj/blessed) - TUI library
  - [Chalk](https://github.com/chalk/chalk) - Terminal colors
  - [node-mpv](https://github.com/j-holub/Node-MPV) - MPV bindings
  - [Winston](https://github.com/winstonjs/winston) - Logging
  - [Zod](https://github.com/colinhacks/zod) - Schema validation

---

## 📞 Support & Community

- **Issues**: [GitHub Issues](https://github.com/HollyTotoC/lofigirl-terminal/issues)
- **Discussions**: [GitHub Discussions](https://github.com/HollyTotoC/lofigirl-terminal/discussions)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

---

<div align="center">

**Made with ❤️ by the community**

**Migrated to Node.js/TypeScript for better cross-platform support** 🚀

[Report Bug](https://github.com/HollyTotoC/lofigirl-terminal/issues) • [Request Feature](https://github.com/HollyTotoC/lofigirl-terminal/issues) • [Documentation](./docs/)

</div>
