# 🔄 Migration Guide: Python → Node.js/TypeScript

## Overview

LofiGirl Terminal has been migrated from **Python** to **Node.js/TypeScript** for better cross-platform compatibility, especially on Windows PowerShell.

## Why Migrate?

### Problems with Python Version
1. ❌ **Complex Windows Setup**: Virtual environments confusing for beginners
2. ❌ **PowerShell Issues**: Limited native support
3. ❌ **MPV Dependencies**: libmpv-2.dll issues on Windows
4. ❌ **Path Management**: Adding to PATH requires manual steps
5. ❌ **Global Install**: Requires pipx or manual launcher scripts

### Benefits of Node.js Version
1. ✅ **Native Cross-Platform**: npm works identically everywhere
2. ✅ **PowerShell First-Class**: Full PowerShell support
3. ✅ **Simple Install**: `npm install -g` works everywhere
4. ✅ **No Virtual Environments**: Simpler dependency management
5. ✅ **Better TypeScript**: Type safety built-in
6. ✅ **Active Ecosystem**: Huge npm package ecosystem

## Side-by-Side Comparison

### Installation

| Python | Node.js |
|--------|---------|
| `pip install` + venv setup | `npm install` |
| Manual PATH addition | Auto-added to PATH |
| Platform-specific scripts | Universal npm commands |
| ~5-7 steps | ~2 steps |

### Usage

```bash
# Python version
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e .
python -m lofigirl_terminal.main tui

# Node.js version
npm install
npm run build
node dist/index.js tui
# or after global install:
lofigirl tui
```

## Migration Process

### For Users

If you have the Python version installed:

1. **Uninstall Python version:**
   ```bash
   # Linux/Mac
   bash ~/.lofigirl-terminal/uninstall.sh

   # Windows PowerShell
   Remove-Item $env:USERPROFILE\lofigirl-terminal -Recurse
   ```

2. **Install Node.js version:**
   ```bash
   # Windows PowerShell
   irm https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install-node.ps1 | iex

   # Linux/Mac
   curl -sSL https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install-node.sh | bash
   ```

3. **Done!** All your preferences are preserved (MPV config, etc.)

### For Developers

#### Prerequisites

Install Node.js 14+:
- **Windows**: Download from [nodejs.org](https://nodejs.org/) or `choco install nodejs`
- **Mac**: `brew install node`
- **Linux**: `sudo apt install nodejs npm` or equivalent

#### Setup Development Environment

```bash
# Clone repository (or use existing)
git clone https://github.com/HollyTotoC/lofigirl-terminal.git
cd lofigirl-terminal

# Install dependencies
npm install

# Build TypeScript
npm run build

# Run
node dist/index.js tui

# Or development mode
npm run dev
```

#### Code Structure Mapping

| Python File | Node.js File | Notes |
|-------------|--------------|-------|
| `src/lofigirl_terminal/main.py` | `src/index.ts` + `src/cli.ts` | Entry point + CLI |
| `src/lofigirl_terminal/config.py` | `src/config.ts` | Pydantic → Zod |
| `src/lofigirl_terminal/logger.py` | `src/logger.ts` | colorlog → winston |
| `src/lofigirl_terminal/modules/stations.py` | `src/modules/stations.ts` | Direct port |
| `src/lofigirl_terminal/modules/player_mpv.py` | `src/modules/player.ts` | python-mpv → node-mpv |
| `src/lofigirl_terminal/tui_rice.py` | `src/modules/tui.ts` | textual → blessed |

#### Library Mapping

| Python | Node.js | Purpose |
|--------|---------|---------|
| `click` | `commander` | CLI framework |
| `rich` | `chalk` + `cli-table3` + `boxen` | Terminal output |
| `textual` | `blessed` | TUI framework |
| `python-mpv` | `node-mpv` | MPV bindings |
| `yt-dlp` (Python) | `ytdl-core` | YouTube downloader |
| `pydantic` | `zod` | Schema validation |
| `python-dotenv` | `dotenv` | Environment variables |
| `colorlog` | `winston` | Logging |
| `pytest` | `jest` | Testing |

## Feature Parity

### ✅ Completed Features

- [x] CLI with all commands (play, list, info, station-info, tui)
- [x] Station management
- [x] Configuration via .env
- [x] Logging system
- [x] TUI interface with blessed
- [x] Cross-platform installers (PowerShell + Bash)
- [x] MPV audio player integration

### 🚧 Work in Progress

- [ ] Advanced TUI features (waveform visualization)
- [ ] YouTube streaming (ytdl-core integration)
- [ ] npm package publication
- [ ] Automated tests

### 📅 Future Enhancements

- [ ] Electron wrapper (optional GUI)
- [ ] Windows Store package
- [ ] Homebrew formula
- [ ] APT/YUM packages

## Troubleshooting

### Node.js Version Issues

```bash
# Check Node.js version
node --version  # Should be v14+

# Update Node.js
# Windows: Download from nodejs.org
# Mac: brew upgrade node
# Linux: Use nvm or package manager
```

### MPV Not Found

```bash
# Windows
choco install mpv

# Mac
brew install mpv

# Linux
sudo apt install mpv  # or equivalent
```

### Build Errors

```bash
# Clean and rebuild
npm run clean
npm install
npm run build
```

### Permission Errors

```bash
# Windows PowerShell (run as Administrator)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Linux/Mac
chmod +x ~/.local/bin/lofigirl
```

## Contributing

The Node.js/TypeScript codebase is more accessible to contributors:

1. **Better Type Safety**: TypeScript catches errors at compile time
2. **Familiar Tools**: npm, Jest, ESLint are widely known
3. **Cross-Platform**: Test on any platform easily
4. **Modern JS**: async/await, ES modules

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## FAQ

### Q: Will Python version still be maintained?

No, we're fully migrating to Node.js for better cross-platform support. The Python version will remain in git history but won't receive updates.

### Q: Do I need to reinstall everything?

Yes, but it's simpler now! Just run the Node.js installer and you're done.

### Q: What about my custom stations?

Custom stations will need to be re-added in the new version. We're working on a migration script.

### Q: Can I use both versions?

Technically yes, but they'll use different installation directories. Not recommended.

### Q: Is performance better?

Node.js startup is slightly faster, and memory usage is similar. Audio playback performance is identical (both use MPV).

## Timeline

- **2024-11**: Python version developed
- **2025-11**: Migration to Node.js started
- **2025-11**: Node.js version completed ✅
- **2025-12**: npm package publication (planned)
- **2026-01**: Python version archived

## Links

- **Python Version** (archived): See git history
- **Node.js Version** (current): Main branch
- **Documentation**: [README-NODE.md](README-NODE.md)
- **Issues**: [GitHub Issues](https://github.com/HollyTotoC/lofigirl-terminal/issues)

---

**Questions?** Open an issue or discussion on GitHub!
