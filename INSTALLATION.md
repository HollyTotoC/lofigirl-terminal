# 📦 Installation Guide - LofiGirl Terminal

Complete installation guide for LofiGirl Terminal with various installation methods.

## 🚀 Quick Install (Recommended)

### One-Line Install

The easiest way to install LofiGirl Terminal:

```bash
curl -sSL https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install.sh | bash
```

**What this does:**
1. ✅ Checks system requirements (Python 3.8+, Git, MPV)
2. ✅ Clones repository to `~/.lofigirl-terminal`
3. ✅ Creates isolated virtual environment
4. ✅ Installs all dependencies
5. ✅ Creates global launcher at `~/.local/bin/lofigirl`
6. ✅ Adds to PATH automatically

**Then simply:**
```bash
lofigirl tui
```

### Update Existing Installation

If you've already installed with the script, simply run it again:

```bash
curl -sSL https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install.sh | bash
```

It will detect the existing installation and update it.

## 🗑️ Uninstall

To completely remove LofiGirl Terminal:

```bash
bash ~/.lofigirl-terminal/uninstall.sh
```

**What this removes:**
- Installation directory (`~/.lofigirl-terminal`)
- Launcher script (`~/.local/bin/lofigirl`)
- Configuration files (optional, asks first)
- PATH entries (optional, asks first)

## 📋 System Requirements

### Required

- **Python**: 3.8 or higher
- **Git**: Any recent version
- **MPV**: Media player for audio/video playback

### Optional

- **yt-dlp**: Automatically installed via pip
- **Terminal**: Any modern terminal emulator

## 🔧 Installing Prerequisites

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git mpv
```

### macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install requirements
brew install python git mpv
```

### Windows

#### Using Chocolatey (Recommended)

```powershell
# Install Chocolatey if not installed
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install requirements
choco install python git mpv
```

#### Manual Installation

1. **Python**: Download from [python.org](https://www.python.org/downloads/)
2. **Git**: Download from [git-scm.com](https://git-scm.com/download/win)
3. **MPV**: Download from [mpv.io](https://mpv.io/installation/)

## 📦 Manual Installation

If you prefer manual installation or the automatic script doesn't work:

### 1. Clone Repository

```bash
git clone https://github.com/HollyTotoC/lofigirl-terminal.git
cd lofigirl-terminal
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

### 4. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements/base.txt

# Install package in development mode
pip install -e .
```

### 5. Verify Installation

```bash
lofigirl --version
lofigirl list
```

## 🎯 Installation via Make

If you're developing or want more control:

```bash
# Complete setup (recommended for developers)
make setup

# Or step by step:
make venv              # Create virtual environment
make install-dev       # Install with dev dependencies
make pre-commit-install # Set up git hooks
```

## 🌐 Using Different Installation Locations

### Custom Installation Directory

```bash
# Edit the install script or set environment variable
export LOFIGIRL_INSTALL_DIR="$HOME/custom/path"
curl -sSL https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install.sh | bash
```

### System-Wide Installation (Not Recommended)

```bash
# Clone repository
sudo git clone https://github.com/HollyTotoC/lofigirl-terminal.git /opt/lofigirl-terminal
cd /opt/lofigirl-terminal

# Create system-wide virtual environment
sudo python3 -m venv /opt/lofigirl-terminal/venv

# Install
sudo /opt/lofigirl-terminal/venv/bin/pip install -r requirements/base.txt
sudo /opt/lofigirl-terminal/venv/bin/pip install -e .

# Create global launcher
sudo ln -s /opt/lofigirl-terminal/venv/bin/lofigirl /usr/local/bin/lofigirl
```

## 🐳 Docker Installation (Coming Soon)

```bash
docker run -it lofigirl/terminal
```

## 📥 Install from PyPI (Coming Soon)

```bash
pip install lofigirl-terminal
```

## 🔍 Troubleshooting

### MPV Not Found

**Error:** `mpv is not installed`

**Solution:**
```bash
# Ubuntu/Debian
sudo apt install mpv

# macOS
brew install mpv

# Windows
choco install mpv
```

### Python Version Too Old

**Error:** `Python 3.8+ required`

**Solution:** Install a newer Python version from [python.org](https://www.python.org/downloads/)

### Permission Denied

**Error:** `Permission denied: '~/.local/bin/lofigirl'`

**Solution:**
```bash
# Make sure ~/.local/bin exists and is writable
mkdir -p ~/.local/bin
chmod 755 ~/.local/bin
```

### Command Not Found After Installation

**Error:** `command not found: lofigirl`

**Solution:**
```bash
# Add to PATH manually
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or use full path
~/.local/bin/lofigirl tui
```

### yt-dlp Errors

**Error:** `yt-dlp extraction failed`

**Solution:**
```bash
# Update yt-dlp
~/.lofigirl-terminal/venv/bin/pip install --upgrade yt-dlp

# Or install system-wide
pip install --upgrade yt-dlp
```

## 🔄 Updating

### Automatic Update

Run the install script again:

```bash
curl -sSL https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install.sh | bash
```

### Manual Update

```bash
cd ~/.lofigirl-terminal
git pull origin main
source venv/bin/activate
pip install --upgrade -r requirements/base.txt
pip install -e .
```

## 🧹 Clean Installation

To start fresh:

```bash
# Uninstall
bash ~/.lofigirl-terminal/uninstall.sh

# Reinstall
curl -sSL https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install.sh | bash
```

## 📊 Verifying Installation

After installation, verify everything works:

```bash
# Check version
lofigirl --version

# List stations
lofigirl list

# Check MPV
mpv --version

# Check yt-dlp
yt-dlp --version

# Launch TUI
lofigirl tui
```

## 💡 Post-Installation Tips

### Set Default Shell Alias

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias lofi="lofigirl tui"
alias lofi-play="lofigirl play"
```

### Create Desktop Shortcut

**Linux:**
Create `~/.local/share/applications/lofigirl.desktop`:

```desktop
[Desktop Entry]
Type=Application
Name=LofiGirl Terminal
Comment=Terminal Lofi Radio Player
Exec=/home/YOUR_USERNAME/.local/bin/lofigirl tui
Terminal=true
Icon=audio-headphones
Categories=AudioVideo;Audio;Player;
```

### Configure Autostart

To start automatically when terminal opens, add to `~/.bashrc`:

```bash
# Auto-start LofiGirl (optional)
# lofigirl tui
```

## 🆘 Getting Help

If installation fails:

1. Check [GitHub Issues](https://github.com/HollyTotoC/lofigirl-terminal/issues)
2. Run with debug mode: `bash -x install.sh`
3. Create an issue with installation logs
4. Join [GitHub Discussions](https://github.com/HollyTotoC/lofigirl-terminal/discussions)

## 📖 Further Reading

- [README.md](README.md) - Main documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contributing guide
- [CLAUDE.md](CLAUDE.md) - Project development tracker

---

**Happy listening! 🎵**
