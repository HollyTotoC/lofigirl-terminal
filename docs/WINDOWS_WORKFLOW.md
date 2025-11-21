# 🪟 Windows PowerShell Workflow - Complete Guide

Step-by-step guide to install and use LofiGirl Terminal on Windows with PowerShell exclusively.

---

## 📦 **Installation (One-Time Setup)**

### **Step 1: Automatic Installation**

Open **PowerShell** and run:

```powershell
irm https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install.ps1 | iex
```

**What the installer does:**
1. ✅ Detects Python (`py`, `python`, or `python3`)
2. ✅ Checks Git
3. ✅ Checks MPV (offers installation via Chocolatey if missing)
4. ✅ Clones project to `C:\Users\YourName\lofigirl-terminal`
5. ✅ Creates Python virtual environment
6. ✅ Installs all dependencies
7. ⚠️ **WARNS** if `libmpv-2.dll` is missing

---

### **Step 2: Fix libmpv-2.dll (If Needed)**

**Symptom**: The installer displays a yellow warning about `libmpv-2.dll`.

#### **Quick Solution (5 minutes)**

1. **Download MPV with libmpv**:
   - Go to: https://github.com/shinchiro/mpv-winbuild-cmake/releases
   - Download: `mpv-x86_64-v3-YYYYMMDD-git-XXXXXXX.7z` (latest version)
   - Example: `mpv-x86_64-v3-20241117-git-d2a8820.7z`

2. **Extract the archive**:
   - Install 7-Zip if needed: `choco install 7zip -y`
   - Right-click → 7-Zip → Extract Here

3. **Copy the DLL**:
   ```powershell
   # Find MPV folder
   $mpvPath = (Get-Command mpv.exe).Source | Split-Path

   # Copy libmpv-2.dll (adjust path to your extraction)
   Copy-Item "C:\Users\YourName\Downloads\mpv-x86_64...\libmpv-2.dll" -Destination $mpvPath

   # Verify
   Get-ChildItem "$mpvPath\libmpv-2.dll"
   ```

4. **Done!** ✅

**Detailed guide**: [Windows Installation Guide](WINDOWS_INSTALL.md)

---

## 🎵 **Usage (Every Time)**

### **Standard Method**

```powershell
# 1. Navigate to project
cd "$env:USERPROFILE\lofigirl-terminal"

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Add MPV to PATH (temporary, for this session)
$env:PATH = "C:\ProgramData\chocolatey\lib\mpvio.install\tools;$env:PATH"

# 4. Launch LofiGirl Terminal (rice style by default)
lofigirl tui
```

**Keyboard shortcuts in TUI:**
- `SPACE` - Play/Pause
- `N` - Next station
- `P` - Previous station
- `M` - Mute/Unmute
- `+` / `-` - Volume +/-
- `Y` - Open in YouTube
- `Q` - Quit

---

### **Quick Method (PowerShell Alias)**

**One-time setup** - Add to your PowerShell profile:

```powershell
# Open your PowerShell profile
notepad $PROFILE

# Add these lines:
function Start-Lofigirl {
    Set-Location "$env:USERPROFILE\lofigirl-terminal"
    .\venv\Scripts\Activate.ps1
    $env:PATH = "C:\ProgramData\chocolatey\lib\mpvio.install\tools;$env:PATH"
    lofigirl tui
}
Set-Alias -Name lofi -Value Start-Lofigirl

# Save and close
```

**Then, every time, just type**:
```powershell
lofi
```

---

### **Permanent PATH (Optional but Recommended)**

To avoid adding MPV to PATH every time:

```powershell
# Open PowerShell as Administrator
# Then run:

[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "Machine") + ";C:\ProgramData\chocolatey\lib\mpvio.install\tools",
    "Machine"
)

# Restart PowerShell
```

**After this, no need for**:
```powershell
$env:PATH = "C:\ProgramData\chocolatey\lib\mpvio.install\tools;$env:PATH"
```

---

## 🎨 **Interface Styles**

LofiGirl Terminal has 2 interface styles:

### **Rice Style (Default)** - Compact, btop-inspired
```powershell
lofigirl tui
# OR explicitly
lofigirl tui --style rice
```

**Features**:
- ✨ Ultra-compact design
- 📊 Real-time waveform (▁▂▃▄▅▆▇█)
- 🎨 Animated ASCII art
- 📋 btop-style info panel
- 🎛️ One-line controls

### **Classic Style** - Full interface
```powershell
lofigirl tui --style classic
```

**Features**:
- 🖼️ Large ASCII art area
- 📊 Detailed visualization
- 🎮 Separated controls
- ℹ️ More information displayed

---

## 📻 **Other Commands**

```powershell
# List all available stations
lofigirl list

# Play specific station (CLI mode, no TUI)
lofigirl play --station lofi-hip-hop

# View station info
lofigirl station-info --station lofi-jazz

# Configure themes and fonts
lofigirl setup

# View all commands
lofigirl --help

# View configuration info
lofigirl info
```

---

## 🎯 **Available Stations**

| ID | Name | Description |
|----|------|-------------|
| `lofi-hip-hop` | 📚 Lofi Hip Hop Radio | Beats to relax/study (default) |
| `lofi-sleep` | 💤 Lofi Sleep Radio | Beats to sleep/chill |
| `synthwave` | 🌌 Synthwave Radio | Beats to chill/game |
| `lofi-jazz` | 🎷 Jazz Lofi Radio | Beats to chill/study |

---

## ⚙️ **Advanced Configuration**

### **Change Theme**

```powershell
# Launch setup wizard
lofigirl setup

# Choose from:
# - Catppuccin Mocha (default)
# - Dracula
# - Nord
# - Tokyo Night
# - Gruvbox
# - Solarized Dark
```

### **Configuration File**

Create/edit: `C:\Users\YourName\.config\lofigirl-terminal\config.env`

```env
# Theme
THEME=catppuccin-mocha

# Default volume
DEFAULT_VOLUME=50

# Default station
DEFAULT_STATION=lofi-hip-hop

# ASCII art
ASCII_ART=lofi-girl-classic

# Font (Nerd Font)
TERMINAL_FONT=JetBrainsMono Nerd Font

# Debug mode
DEBUG_MODE=false
```

---

## 🔄 **Update**

```powershell
# Navigate to project
cd "$env:USERPROFILE\lofigirl-terminal"

# Activate venv
.\venv\Scripts\Activate.ps1

# Update from GitHub
git pull origin main

# Update dependencies
pip install -r requirements\base.txt --upgrade

# Reinstall package
pip install -e .
```

---

## 🗑️ **Uninstall**

```powershell
# Remove project
Remove-Item "$env:USERPROFILE\lofigirl-terminal" -Recurse -Force

# Remove config (optional)
Remove-Item "$env:USERPROFILE\.config\lofigirl-terminal" -Recurse -Force

# Remove alias from PowerShell profile (optional)
notepad $PROFILE
# Delete the Start-Lofigirl alias lines
```

---

## 🐛 **Quick Troubleshooting**

### **Problem: Virtual environment activation fails**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Problem: Python not found**
```powershell
# Check which command works
py --version
python --version
python3 --version

# Use the one that works to create venv
```

### **Problem: MPV not found**
```powershell
# Check installation
where.exe mpv

# Reinstall if needed
choco install mpv -y
```

### **Problem: libmpv-2.dll not found**
See **Step 2** of installation or full guide: [Windows Installation Guide](WINDOWS_INSTALL.md)

### **Problem: yt-dlp errors**
```powershell
pip install --upgrade yt-dlp
```

---

## 📊 **Workflow Summary**

```
┌─────────────────────────────────────────┐
│  1️⃣  INSTALLATION (one time)           │
├─────────────────────────────────────────┤
│  • Run install.ps1                      │
│  • Copy libmpv-2.dll if needed          │
└─────────────────────────────────────────┘
           ⬇️
┌─────────────────────────────────────────┐
│  2️⃣  USAGE (every time)                │
├─────────────────────────────────────────┤
│  • cd lofigirl-terminal                 │
│  • .\venv\Scripts\Activate.ps1          │
│  • $env:PATH = "...\tools;$env:PATH"    │
│  • lofigirl tui                         │
└─────────────────────────────────────────┘
           ⬇️
┌─────────────────────────────────────────┐
│  3️⃣  ENJOY! 🎵                         │
├─────────────────────────────────────────┤
│  • SPACE: play/pause                    │
│  • N/P: next/prev station               │
│  • +/-: volume                          │
│  • Q: quit                              │
└─────────────────────────────────────────┘
```

---

## 💡 **Tips & Tricks**

### **1. Desktop Shortcut**

Create a `LofiGirl.ps1` file on desktop:

```powershell
Set-Location "$env:USERPROFILE\lofigirl-terminal"
.\venv\Scripts\Activate.ps1
$env:PATH = "C:\ProgramData\chocolatey\lib\mpvio.install\tools;$env:PATH"
lofigirl tui
```

### **2. Windows Terminal Integration**

Add to Windows Terminal profile (`settings.json`):

```json
{
  "name": "LofiGirl Terminal",
  "commandline": "powershell.exe -NoExit -Command \"cd $env:USERPROFILE\\lofigirl-terminal; .\\venv\\Scripts\\Activate.ps1; $env:PATH = 'C:\\ProgramData\\chocolatey\\lib\\mpvio.install\\tools;' + $env:PATH; lofigirl tui\"",
  "icon": "🎵"
}
```

### **3. Launch at Windows Startup**

Add shortcut to:
```
C:\Users\YourName\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\
```

---

**🎉 Enjoy your lofi sessions! 🎧**

Questions? → [GitHub Issues](https://github.com/HollyTotoC/lofigirl-terminal/issues)
