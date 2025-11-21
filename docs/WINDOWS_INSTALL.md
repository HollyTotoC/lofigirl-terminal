# 🪟 Windows Installation Guide

Complete guide for installing LofiGirl Terminal on Windows, including fixing the libmpv-2.dll issue with Chocolatey.

## Quick Install (PowerShell)

Open PowerShell and run:

```powershell
irm https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install.ps1 | iex
```

---

## ⚠️ Common Issue: Missing libmpv-2.dll

**Problem**: When you run `lofigirl tui`, you get this error:
```
Error: Cannot find mpv-1.dll, mpv-2.dll or libmpv-2.dll in your system %PATH%
```

**Cause**: Chocolatey's MPV package (`mpvio.install` or `mpv`) includes `mpv.exe` but **not** the `libmpv-2.dll` library that Python needs.

---

## ✅ Solution: Install libmpv-2.dll Manually

### Option 1: Download from GitHub (Recommended)

1. **Download MPV with libmpv**
   - Visit: https://github.com/shinchiro/mpv-winbuild-cmake/releases
   - Download the latest: `mpv-x86_64-v3-YYYYMMDD-git-XXXXXXX.7z`
   - Example: `mpv-x86_64-v3-20241117-git-d2a8820.7z`

2. **Extract the archive**
   - Use 7-Zip (install with: `choco install 7zip -y`)
   - Right-click → 7-Zip → Extract Here

3. **Copy libmpv-2.dll**
   - Find `libmpv-2.dll` in the extracted folder
   - Copy it to MPV's installation directory:
     ```
     C:\ProgramData\chocolatey\lib\mpvio.install\tools\
     ```

4. **Verify the DLL is there**
   ```powershell
   Get-ChildItem "C:\ProgramData\chocolatey\lib\mpvio.install\tools\libmpv-2.dll"
   ```

### Option 2: Download from SourceForge

1. Visit: https://sourceforge.net/projects/mpv-player-windows/files/libmpv/
2. Download the latest version
3. Extract and copy `libmpv-2.dll` to MPV's folder (see above)

### Option 3: Use Scoop (Alternative Package Manager)

If you prefer, you can use Scoop which includes libmpv by default:

```powershell
# Install Scoop
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
irm get.scoop.sh | iex

# Install MPV (includes libmpv-2.dll)
scoop install mpv

# Add to PATH
$env:PATH = "$env:USERPROFILE\scoop\apps\mpv\current;$env:PATH"
```

---

## 🔧 Manual Installation (Without installer script)

If you prefer to install manually:

### 1. Prerequisites

- **Python 3.8+**: https://www.python.org/downloads/
  - ✅ Check "Add Python to PATH" during installation
- **Git**: https://git-scm.com/download/win
- **MPV**: `choco install mpv -y` (then add libmpv-2.dll manually)
- **7-Zip**: `choco install 7zip -y` (for extracting archives)

### 2. Clone and Install

```powershell
# Clone repository
git clone https://github.com/HollyTotoC/lofigirl-terminal.git
cd lofigirl-terminal

# Create virtual environment (use py, python, or python3)
py -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements\base.txt

# Install package
pip install -e .

# Run setup
lofigirl setup

# Launch rice-style TUI
lofigirl tui
```

### 3. Add MPV to PATH (For Current Session)

```powershell
$env:PATH = "C:\ProgramData\chocolatey\lib\mpvio.install\tools;$env:PATH"
```

### 4. Add MPV to PATH (Permanent)

Run in PowerShell as **Administrator**:

```powershell
[Environment]::SetEnvironmentVariable(
    "Path",
    [Environment]::GetEnvironmentVariable("Path", "Machine") + ";C:\ProgramData\chocolatey\lib\mpvio.install\tools",
    "Machine"
)
```

Then **restart PowerShell** for changes to take effect.

---

## 🎵 Running LofiGirl Terminal

### Every Time (If not using permanent PATH)

```powershell
# 1. Navigate to project
cd "$env:USERPROFILE\lofigirl-terminal"

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Add MPV to PATH (if not permanent)
$env:PATH = "C:\ProgramData\chocolatey\lib\mpvio.install\tools;$env:PATH"

# 4. Run lofigirl
lofigirl tui              # Rice style (compact, btop-inspired)
lofigirl tui --style classic  # Classic style
lofigirl play             # CLI mode
lofigirl list             # List stations
```

### With PowerShell Profile (Recommended)

Add to your PowerShell profile (`$PROFILE`) to auto-activate:

```powershell
# Add this to your profile
function Start-Lofigirl {
    Set-Location "$env:USERPROFILE\lofigirl-terminal"
    .\venv\Scripts\Activate.ps1
    $env:PATH = "C:\ProgramData\chocolatey\lib\mpvio.install\tools;$env:PATH"
    lofigirl tui
}

Set-Alias -Name lofi -Value Start-Lofigirl
```

Then just type `lofi` in any PowerShell window!

---

## 🐛 Troubleshooting

### Python not found

```powershell
# Check Python installation
py --version
python --version
python3 --version

# If none work, reinstall Python from python.org
# Make sure to check "Add Python to PATH"
```

### Virtual environment activation fails

```powershell
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again
.\venv\Scripts\Activate.ps1
```

### MPV not found

```powershell
# Check if MPV is installed
where.exe mpv

# If not found, install with Chocolatey
choco install mpv -y
```

### libmpv-2.dll still not found

```powershell
# Verify DLL exists
$mpvPath = (Get-Command mpv.exe).Source | Split-Path
Get-ChildItem "$mpvPath\*.dll"

# Should show libmpv-2.dll
# If not, follow "Option 1: Download from GitHub" above
```

### yt-dlp errors

```powershell
# Update yt-dlp
pip install --upgrade yt-dlp
```

---

## 📦 Alternative: Install without Chocolatey

If you don't want to use Chocolatey:

1. **Install Python** manually from https://www.python.org/
2. **Install Git** from https://git-scm.com/
3. **Download MPV with libmpv**:
   - https://github.com/shinchiro/mpv-winbuild-cmake/releases
   - Extract to a folder like `C:\mpv\`
4. **Add MPV to PATH**:
   ```powershell
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\mpv", "User")
   ```
5. Follow the manual installation steps above

---

## 🆘 Still Having Issues?

1. Check the logs:
   ```powershell
   Get-Content "$env:USERPROFILE\.lofigirl-terminal\logs\lofigirl.log"
   ```

2. Open an issue: https://github.com/HollyTotoC/lofigirl-terminal/issues

3. Include:
   - Windows version (`winver`)
   - Python version (`py --version`)
   - MPV version (`mpv --version`)
   - Error message
   - Whether libmpv-2.dll exists in MPV folder

---

## 🎉 Enjoy!

Once installed, you can:
- `lofigirl tui` - Launch the beautiful rice-style interface
- `lofigirl setup` - Change themes and fonts
- `lofigirl list` - See all available stations
- `lofigirl play` - Play in CLI mode
- `lofigirl --help` - See all commands

**Happy listening!** 🎵🎧
