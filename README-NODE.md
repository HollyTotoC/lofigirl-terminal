# 🎵 LofiGirl Terminal (Node.js/TypeScript)

<div align="center">

[![Node.js 14+](https://img.shields.io/badge/node-%3E%3D14.0.0-brightgreen.svg)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue.svg)](https://www.typescriptlang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Cross-platform terminal-based lofi radio player**
Works natively on PowerShell (Windows), Terminal (Mac), and Linux!

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Development](#-development)

</div>

---

## 📖 About

**LofiGirl Terminal** has been migrated from Python to **Node.js/TypeScript** for true cross-platform compatibility! Now you can run it natively on:

- ✅ **Windows PowerShell** - Native support
- ✅ **macOS Terminal** - Native support
- ✅ **Linux Terminal** - Native support

No Python required! Just Node.js and you're ready to go.

### ✨ Features

#### 🎵 Audio Streaming
- 🎧 **Real YouTube Streaming**: Direct integration with LofiGirl channels
- 📻 **Multiple Stations**: 4 curated lofi stations (hip-hop, sleep, jazz, study)
- 🎛️ **Full Playback Control**: Play, pause, stop, next/previous
- 🔊 **Volume Management**: Volume control, mute, adjustable levels

#### 🎨 Interactive TUI
- 🖼️ **Blessed TUI**: Cross-platform terminal interface
- 📊 **Real-time Status**: Live playback status and volume display
- ⌨️ **Keyboard Shortcuts**: SPACE, N, P, M, +/-, Q
- 🎨 **Colorful Display**: Rich colors with chalk

#### 🛠️ Technical
- ⚡ **TypeScript**: Fully typed for better development experience
- 🌍 **Cross-platform**: Works on Windows, Mac, Linux natively
- 📦 **npm Package**: Easy global installation
- 🔌 **MPV Backend**: Professional audio playback
- ⚙️ **Configurable**: .env file for settings

## 🚀 Installation

### Prerequisites

- **Node.js 14+** (LTS recommended)
- **npm** (comes with Node.js)
- **MPV media player** (for audio playback)
- **Git**

### 🪟 Windows (PowerShell)

Install with a single PowerShell command:

```powershell
irm https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install-node.ps1 | iex
```

This will:
- ✅ Check Node.js installation
- ✅ Check/install MPV
- ✅ Clone repository
- ✅ Install npm dependencies
- ✅ Build TypeScript
- ✅ Create launcher in PATH

**Then run:**
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
- ✅ Check/install MPV
- ✅ Clone repository to `~/.lofigirl-terminal`
- ✅ Install npm dependencies
- ✅ Build TypeScript
- ✅ Create launcher at `~/.local/bin/lofigirl`

**Then run:**
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

# Build TypeScript
npm run build

# Run
node dist/index.js tui
```

### 🌐 Global Installation (from npm - Coming Soon)

```bash
npm install -g lofigirl-terminal
```

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
- `+/-` - Volume up/down
- `Q` - Quit

### 📟 CLI Commands

```bash
# Show help
lofigirl --help

# Launch TUI
lofigirl tui

# List available stations
lofigirl list

# Play default station
lofigirl play

# Play specific station
lofigirl play --station lofi-jazz

# Play with custom volume
lofigirl play --volume 75

# Show app info
lofigirl info

# Get station details
lofigirl station-info --station lofi-hip-hop
```

### Available Stations

- **lofi-hip-hop**: 24/7 chill lofi hip hop beats
- **lofi-jazz**: Smooth jazz with lofi aesthetics
- **lofi-sleep**: Calming beats for sleep
- **lofi-study**: Focus-enhancing beats

### Configuration

Create a `.env` file in the installation directory:

```env
# Application Settings
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR
DEFAULT_VOLUME=50           # 0-100
AUDIO_QUALITY=high          # low, medium, high
DEFAULT_STATION=lofi-hip-hop

# UI Settings
THEME=default
SHOW_VISUALIZER=true
UPDATE_INTERVAL=1           # seconds
```

## 🛠️ Development

### Setup

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
```

### Project Structure

```
lofigirl-terminal/
├── src/
│   ├── index.ts              # Entry point
│   ├── cli.ts                # CLI commands (Commander.js)
│   ├── config.ts             # Configuration (Zod)
│   ├── logger.ts             # Logging (Winston)
│   ├── types.ts              # TypeScript types
│   └── modules/
│       ├── stations.ts       # Station management
│       ├── player.ts         # MPV player wrapper
│       └── tui.ts            # TUI interface (blessed)
├── dist/                     # Compiled JavaScript
├── package.json              # npm configuration
├── tsconfig.json             # TypeScript config
├── install-node.ps1          # PowerShell installer
├── install-node.sh           # Bash installer
└── README-NODE.md            # This file
```

### Technology Stack

| Component | Library |
|-----------|---------|
| Language | TypeScript 5.3 |
| CLI Framework | Commander.js |
| TUI | Blessed |
| Terminal Colors | Chalk |
| Audio Player | node-mpv |
| YouTube Streaming | ytdl-core |
| Configuration | Zod + dotenv |
| Logging | Winston |

## 🔄 Migration from Python

This project has been migrated from Python to Node.js/TypeScript for better cross-platform support. Key changes:

### Why Node.js?

1. **Native Cross-Platform**: npm works identically on Windows, Mac, Linux
2. **No Virtual Environments**: Simpler dependency management
3. **Global Installation**: `npm install -g` works everywhere
4. **Better Windows Support**: PowerShell is first-class citizen
5. **Active Ecosystem**: Large community and package ecosystem

### Python vs Node.js Comparison

| Feature | Python | Node.js |
|---------|--------|---------|
| Installation | pip + venv | npm (built-in) |
| Windows Support | Complex | Native |
| PowerShell Support | Limited | Excellent |
| Global CLI | pipx needed | npm -g native |
| Dependencies | requirements.txt | package.json |
| Type System | mypy (optional) | TypeScript (native) |

## 🤝 Contributing

Contributions welcome! The TypeScript codebase is easier to understand and contribute to.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run linter: `npm run lint`
5. Build: `npm run build`
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Open a Pull Request

## 📋 Roadmap

### ✅ Completed (Node.js Migration)
- [x] TypeScript project setup
- [x] Core modules migration (config, stations, player)
- [x] CLI with Commander.js
- [x] TUI with blessed
- [x] PowerShell installer
- [x] Bash installer
- [x] Cross-platform testing

### 🚧 In Progress
- [ ] npm package publication
- [ ] Enhanced TUI with blessed-contrib
- [ ] Audio visualizations

### 📅 Planned
- [ ] Windows Store package
- [ ] Homebrew formula (Mac)
- [ ] APT/YUM packages (Linux)
- [ ] Electron wrapper (optional GUI)
- [ ] Custom station management
- [ ] Playlist/favorites system

## 🐛 Known Issues

- MPV must be installed separately (auto-install coming soon)
- Some YouTube URLs may require updates

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- Original Python version contributors
- [Lofi Girl](https://www.youtube.com/c/LofiGirl) YouTube channel
- Built with:
  - [Commander.js](https://github.com/tj/commander.js/) - CLI
  - [Blessed](https://github.com/chjj/blessed) - TUI
  - [Chalk](https://github.com/chalk/chalk) - Colors
  - [node-mpv](https://github.com/j-holub/Node-MPV) - Audio player
  - [Winston](https://github.com/winstonjs/winston) - Logging

---

<div align="center">

**Made with ❤️ for the lofi community**

[Report Bug](https://github.com/HollyTotoC/lofigirl-terminal/issues) • [Request Feature](https://github.com/HollyTotoC/lofigirl-terminal/issues)

</div>
