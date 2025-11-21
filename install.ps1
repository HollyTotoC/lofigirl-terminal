# LofiGirl Terminal - PowerShell Installation Script
# Compatible Windows 10/11, PowerShell 5.1+
# Usage: irm https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install.ps1 | iex

#Requires -Version 5.1

$ErrorActionPreference = "Stop"

# Colors
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    try {
        $host.UI.RawUI.ForegroundColor = $ForegroundColor
        if ($args) {
            Write-Output $args
        }
    } finally {
        $host.UI.RawUI.ForegroundColor = $fc
    }
}

function Write-Info($msg) {
    Write-ColorOutput Cyan "ℹ️  $msg"
}

function Write-Success($msg) {
    Write-ColorOutput Green "✓ $msg"
}

function Write-Warning($msg) {
    Write-ColorOutput Yellow "⚠️  $msg"
}

function Write-Error($msg) {
    Write-ColorOutput Red "✗ $msg"
}

function Write-Header {
    Write-ColorOutput Cyan @"

╔════════════════════════════════════════════╗
║   🎵 LofiGirl Terminal Installer 🎵       ║
║   Terminal Lofi Radio Player              ║
╚════════════════════════════════════════════╝

"@
}

# Find Python command (py, python, python3)
function Find-Python {
    Write-Info "Detecting Python installation..."

    $pythonCommands = @("py", "python", "python3")

    foreach ($cmd in $pythonCommands) {
        try {
            $version = & $cmd --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Found Python: $cmd ($version)"
                return $cmd
            }
        } catch {
            continue
        }
    }

    Write-Error "Python not found. Please install Python 3.8+ from https://www.python.org/"
    Write-Info "Make sure to check 'Add Python to PATH' during installation"
    exit 1
}

# Check if command exists
function Test-Command($cmd) {
    try {
        Get-Command $cmd -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# Check system requirements
function Test-Requirements {
    Write-Info "Checking system requirements..."

    # Check Git
    if (Test-Command "git") {
        $gitVersion = git --version
        Write-Success "Git found: $gitVersion"
    } else {
        Write-Error "Git is not installed"
        Write-Info "Download from: https://git-scm.com/download/win"
        exit 1
    }

    # Check MPV
    if (Test-Command "mpv") {
        Write-Success "MPV found"

        # Check if libmpv-2.dll is available
        $mpvPath = (Get-Command mpv.exe).Source | Split-Path
        $libmpvPath = Join-Path $mpvPath "libmpv-2.dll"

        if (-not (Test-Path $libmpvPath)) {
            Write-Warning "libmpv-2.dll not found - Python integration requires it"
            Write-Info ""
            Write-ColorOutput Yellow @"
⚠️  IMPORTANT: Chocolatey's MPV package may not include libmpv-2.dll
   which is required for Python integration.

   If lofigirl fails with 'Cannot find libmpv-2.dll' error:

   1. Download MPV with libmpv from:
      https://github.com/shinchiro/mpv-winbuild-cmake/releases

   2. Extract the archive and copy libmpv-2.dll to:
      $mpvPath

   3. Or see: https://github.com/HollyTotoC/lofigirl-terminal/blob/main/docs/WINDOWS_INSTALL.md

"@
            Write-Info ""
            Read-Host "Press Enter to continue"
        }
    } else {
        Write-Warning "MPV not found - required for audio playback"
        Write-Info "Install with: choco install mpv -y"
        Write-Info ""

        $response = Read-Host "Would you like to install MPV now? (Y/n)"
        if ($response -eq "" -or $response -eq "Y" -or $response -eq "y") {
            if (Test-Command "choco") {
                Write-Info "Installing MPV via Chocolatey..."
                choco install mpv -y

                Write-Info ""
                Write-ColorOutput Yellow @"
⚠️  IMPORTANT NOTE: The Chocolatey MPV package may not include libmpv-2.dll

   After installation, you may need to manually add libmpv-2.dll:

   1. Download from: https://github.com/shinchiro/mpv-winbuild-cmake/releases
   2. Extract and copy libmpv-2.dll to MPV's installation folder
   3. See detailed instructions: https://github.com/HollyTotoC/lofigirl-terminal/blob/main/docs/WINDOWS_INSTALL.md

"@
                Write-Info ""
                Read-Host "Press Enter to continue"
            } else {
                Write-Warning "Chocolatey not found. Please install MPV manually."
                Write-Info "Visit: https://mpv.io/installation/"
                $continue = Read-Host "Continue without MPV? (y/N)"
                if ($continue -ne "y" -and $continue -ne "Y") {
                    exit 1
                }
            }
        }
    }

    # Check yt-dlp
    if (Test-Command "yt-dlp") {
        Write-Success "yt-dlp found"
    } else {
        Write-Warning "yt-dlp not found - will be installed via pip"
    }
}

# Main installation
function Install-LofiGirl {
    param($PythonCmd)

    $installDir = "$env:USERPROFILE\lofigirl-terminal"
    $venvDir = "$installDir\venv"

    Write-Info "Installing LofiGirl Terminal to: $installDir"

    # Clone or update repository
    if (Test-Path "$installDir\.git") {
        Write-Info "Repository exists, updating..."
        Push-Location $installDir
        git fetch origin
        git reset --hard origin/main
        Pop-Location
        Write-Success "Repository updated"
    } else {
        Write-Info "Cloning repository..."
        if (Test-Path $installDir) {
            Remove-Item $installDir -Recurse -Force
        }
        git clone "https://github.com/HollyTotoC/lofigirl-terminal.git" $installDir
        Write-Success "Repository cloned"
    }

    # Create virtual environment
    Write-Info "Creating virtual environment..."
    if (Test-Path $venvDir) {
        Write-Info "Removing old virtual environment..."
        Remove-Item $venvDir -Recurse -Force
    }

    Push-Location $installDir
    & $PythonCmd -m venv venv
    Write-Success "Virtual environment created"

    # Activate virtual environment
    $activateScript = "$venvDir\Scripts\Activate.ps1"
    . $activateScript

    # Upgrade pip
    Write-Info "Upgrading pip..."
    & python -m pip install --upgrade pip setuptools wheel --quiet

    # Install dependencies
    Write-Info "Installing dependencies..."
    & pip install -r requirements\base.txt --quiet
    & pip install -e . --quiet
    Write-Success "Dependencies installed"

    Pop-Location
}

# Create launcher script
function New-Launcher {
    $binDir = "$env:USERPROFILE\.local\bin"

    if (-not (Test-Path $binDir)) {
        New-Item -ItemType Directory -Path $binDir -Force | Out-Null
    }

    $launcherPath = "$binDir\lofigirl.ps1"

    $launcherContent = @'
#!/usr/bin/env pwsh
# LofiGirl Terminal Launcher

$installDir = "$env:USERPROFILE\lofigirl-terminal"
$venvDir = "$installDir\venv"

if (-not (Test-Path $installDir)) {
    Write-Error "LofiGirl Terminal is not installed"
    Write-Host "Run installation script from: https://github.com/HollyTotoC/lofigirl-terminal"
    exit 1
}

# Activate virtual environment and run
$activateScript = "$venvDir\Scripts\Activate.ps1"
. $activateScript

# Add MPV to PATH if needed
$mpvPath = "C:\ProgramData\chocolatey\lib\mpvio.install\tools"
if (Test-Path $mpvPath) {
    $env:PATH = "$mpvPath;$env:PATH"
}

# Run lofigirl with arguments
& python -m lofigirl_terminal.main $args
'@

    Set-Content -Path $launcherPath -Value $launcherContent
    Write-Success "Launcher created at: $launcherPath"

    # Create alias in PowerShell profile
    $profileDir = Split-Path $PROFILE
    if (-not (Test-Path $profileDir)) {
        New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    }

    if (-not (Test-Path $PROFILE)) {
        New-Item -ItemType File -Path $PROFILE -Force | Out-Null
    }

    $aliasLine = "Set-Alias -Name lofigirl -Value '$launcherPath'"
    $profileContent = Get-Content $PROFILE -ErrorAction SilentlyContinue

    if (-not ($profileContent | Select-String -Pattern 'Set-Alias\s+-Name\s+lofigirl')) {
        Add-Content -Path $PROFILE -Value "`n# LofiGirl Terminal"
        Add-Content -Path $PROFILE -Value $aliasLine
        Write-Success "Added alias to PowerShell profile"
    }
}

# Run setup wizard
function Start-SetupWizard {
    Write-Host ""
    Write-ColorOutput Cyan "🎨 Let's customize your LofiGirl Terminal experience!"
    Write-Host ""

    $response = Read-Host "Would you like to configure themes and fonts now? (Y/n)"

    if ($response -eq "" -or $response -eq "Y" -or $response -eq "y") {
        Write-Info "Running setup wizard..."
        Write-Host ""

        $installDir = "$env:USERPROFILE\lofigirl-terminal"
        $activateScript = "$installDir\venv\Scripts\Activate.ps1"
        . $activateScript

        # Add MPV to PATH
        $mpvPath = "C:\ProgramData\chocolatey\lib\mpvio.install\tools"
        if (Test-Path $mpvPath) {
            $env:PATH = "$mpvPath;$env:PATH"
        }

        & python -m lofigirl_terminal.main setup
    } else {
        Write-Info "Skipping setup. You can run it later with: lofigirl setup"
    }
}

# Print completion message
function Show-Completion {
    Write-Host ""
    Write-ColorOutput Green @"
╔════════════════════════════════════════════╗
║     🎉 Installation Complete! 🎉          ║
╚════════════════════════════════════════════╝
"@
    Write-Host ""
    Write-Success "LofiGirl Terminal installed successfully!"
    Write-Host ""
    Write-Info "Quick Start:"
    Write-ColorOutput Cyan "  lofigirl tui        - Launch interactive TUI (recommended)"
    Write-ColorOutput Cyan "  lofigirl setup      - Configure themes and fonts"
    Write-ColorOutput Cyan "  lofigirl list       - List available stations"
    Write-ColorOutput Cyan "  lofigirl play       - Play default station"
    Write-ColorOutput Cyan "  lofigirl --help     - Show all commands"
    Write-Host ""
    Write-Warning "Note: Restart PowerShell or run:"
    Write-ColorOutput Cyan "  . `$PROFILE"
    Write-Host ""
    Write-Info "To uninstall, run:"
    Write-ColorOutput Cyan "  Remove-Item `$env:USERPROFILE\lofigirl-terminal -Recurse"
    Write-Host ""
}

# Main execution
try {
    Write-Header

    $pythonCmd = Find-Python
    Test-Requirements
    Install-LofiGirl -PythonCmd $pythonCmd
    New-Launcher
    Start-SetupWizard
    Show-Completion

} catch {
    Write-Error "Installation failed: $_"
    Write-Host $_.ScriptStackTrace
    exit 1
}
