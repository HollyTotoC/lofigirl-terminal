# 🚀 Quick Start Guide - Node.js Version

## For the Impatient 😄

Want to test the new Node.js version right now? Here's how!

## Prerequisites

Make sure you have:
- ✅ **Node.js 14+** (check: `node --version`)
- ✅ **npm** (check: `npm --version`)
- ✅ **Git** (check: `git --version`)
- ⚠️ **MPV** (optional for audio, check: `mpv --version`)

Don't have Node.js? Install it:
- **Windows**: [nodejs.org](https://nodejs.org/) or `choco install nodejs`
- **Mac**: `brew install node`
- **Linux**: `sudo apt install nodejs npm` or equivalent

## 3-Step Setup

### 1. Clone & Enter

```bash
git clone https://github.com/HollyTotoC/lofigirl-terminal.git
cd lofigirl-terminal
```

### 2. Install & Build

```bash
npm install
npm run build
```

This takes ~30 seconds.

### 3. Test It!

```bash
# Show version
node dist/index.js --version

# List stations
node dist/index.js list

# Show config
node dist/index.js info

# Get station details
node dist/index.js station-info --station lofi-jazz

# Launch TUI (interactive)
node dist/index.js tui
```

## Expected Output

### Version Command
```bash
$ node dist/index.js --version
0.2.0
```

### List Command
```bash
$ node dist/index.js list

✨ Available Lofi Radio Stations

┌────────────────────┬────────────────────────────┬──────────────────┬──────────────────────────────────────────────────┐
│ ID                 │ Name                       │ Genre            │ Description                                      │
├────────────────────┼────────────────────────────┼──────────────────┼──────────────────────────────────────────────────┤
│ lofi-hip-hop       │ Lofi Hip Hop Radio         │ lofi-hip-hop     │ 24/7 chill lofi hip hop beats to study/relax to  │
├────────────────────┼────────────────────────────┼──────────────────┼──────────────────────────────────────────────────┤
│ lofi-sleep         │ Lofi Sleep Radio           │ lofi-sleep       │ Calming lofi beats for sleep and meditation      │
├────────────────────┼────────────────────────────┼──────────────────┼──────────────────────────────────────────────────┤
│ lofi-jazz          │ Lofi Jazz Radio            │ lofi-jazz        │ Smooth jazz with lofi aesthetics                 │
├────────────────────┼────────────────────────────┼──────────────────┼──────────────────────────────────────────────────┤
│ lofi-study         │ Lofi Study Radio           │ lofi-study       │ Focus-enhancing lofi beats for studying          │
└────────────────────┴────────────────────────────┴──────────────────┴──────────────────────────────────────────────────┘

💡 Use 'lofigirl play --station <ID>' to play a station
```

### TUI Command
```bash
$ node dist/index.js tui

╔══════════════════════════════════════════╗
║ 🎵 Starting LofiGirl TUI                 ║
║                                          ║
║ Compact btop-style interface             ║
║ Press 'q' to quit                        ║
╚══════════════════════════════════════════╝

[Interactive TUI launches here]
```

## TUI Controls

When you run `node dist/index.js tui`:

- **SPACE** - Play/Pause
- **N** - Next station
- **P** - Previous station
- **M** - Mute/Unmute
- **+** or **=** - Volume up
- **-** or **_** - Volume down
- **Q** or **Ctrl+C** - Quit

## Installing Globally (Optional)

To use `lofigirl` command anywhere:

```bash
npm link
```

Now you can run:
```bash
lofigirl tui
lofigirl list
lofigirl --help
```

## Development Mode

For active development:

```bash
# Watch mode (auto-rebuild on changes)
npm run build:watch

# In another terminal, run:
npm run dev
```

## Common Issues

### "Cannot find module 'commander'"

**Solution**: Run `npm install`

### "tsc: command not found"

**Solution**: Run `npm install` (TypeScript is in devDependencies)

### "MPV not found"

**Audio playback requires MPV. Install it:**
- **Windows**: `choco install mpv`
- **Mac**: `brew install mpv`
- **Linux**: `sudo apt install mpv`

The TUI will still work without MPV (just no audio).

### "Permission denied" (Linux/Mac)

**Solution**:
```bash
chmod +x install-node.sh
```

## Testing Different Platforms

### Windows PowerShell

```powershell
# Test installation script
.\install-node.ps1

# Or manual install
npm install
npm run build
node dist/index.js list
```

### Mac/Linux Terminal

```bash
# Test installation script
./install-node.sh

# Or manual install
npm install
npm run build
node dist/index.js list
```

## What to Test?

### ✅ Basic Functionality
- [ ] `node dist/index.js --version` shows version
- [ ] `node dist/index.js list` shows 4 stations
- [ ] `node dist/index.js info` shows configuration
- [ ] `node dist/index.js station-info -s lofi-jazz` shows details

### ✅ TUI Interface
- [ ] `node dist/index.js tui` launches TUI
- [ ] Keyboard controls work (SPACE, N, P, M, +/-, Q)
- [ ] Colors and formatting look good
- [ ] No crashes or errors

### ✅ Build System
- [ ] `npm run build` completes without errors
- [ ] `dist/` folder is created
- [ ] All TypeScript files compile

### ✅ Code Quality
- [ ] `npm run lint` passes
- [ ] `npm run format` formats code

### ⚠️ Audio (requires MPV)
- [ ] `node dist/index.js play` starts playback
- [ ] Volume controls work
- [ ] Can pause/resume

## Development Workflow

```bash
# 1. Make changes to src/*.ts files

# 2. Rebuild
npm run build

# 3. Test
node dist/index.js list

# 4. Lint (optional)
npm run lint

# 5. Format (optional)
npm run format
```

## Environment Variables

Create `.env` file for custom settings:

```env
LOG_LEVEL=DEBUG
DEFAULT_VOLUME=75
DEFAULT_STATION=lofi-jazz
THEME=default
```

Then test:
```bash
node dist/index.js info
```

## Need Help?

- 📖 **Full docs**: See [README-NODE.md](README-NODE.md)
- 🔄 **Migration guide**: See [MIGRATION.md](MIGRATION.md)
- 📝 **Summary**: See [MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/HollyTotoC/lofigirl-terminal/issues)

## Performance

- **Install time**: ~30 seconds (npm install)
- **Build time**: ~5 seconds (tsc)
- **Startup time**: <1 second
- **Memory usage**: ~50-80 MB

## Next Steps

After testing:
1. ⭐ Star the repo if you like it!
2. 🐛 Report any bugs you find
3. 💡 Suggest improvements
4. 🤝 Contribute code!

## Comparison: Python vs Node.js

### Installation
```bash
# Python (old)
python -m venv venv
source venv/bin/activate
pip install -r requirements/base.txt
pip install -e .

# Node.js (new)
npm install
npm run build
```

### Running
```bash
# Python (old)
python -m lofigirl_terminal.main tui

# Node.js (new)
node dist/index.js tui
# or after npm link:
lofigirl tui
```

**Winner**: Node.js (simpler!) 🎉

---

**Happy testing!** 🎵

*If you find any issues, please create a GitHub issue with:*
- *Your OS and version*
- *Node.js version (`node --version`)*
- *Error message or screenshot*
- *Steps to reproduce*
