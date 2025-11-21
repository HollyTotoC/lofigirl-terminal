# LofiGirl Terminal - PowerShell Installation Script (Node.js version)
# Compatible Windows 10/11, PowerShell 5.1+
# Usage: irm https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install-node.ps1 | iex

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
║   Cross-Platform Lofi Radio Player        ║
║   (Node.js/TypeScript Edition)            ║
╚════════════════════════════════════════════╝

"@
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

# Find Node.js installation
function Find-Node {
    Write-Info "Detecting Node.js installation..."

    if (Test-Command "node") {
        $version = node --version
        $npmVersion = npm --version
        $majorVersion = [int]($version -replace 'v(\d+)\..*', '$1')

        if ($majorVersion -ge 14) {
            Write-Success "Found Node.js: $version (npm: $npmVersion)"
            return $true
        } else {
            Write-Warning "Node.js version $version found but v14+ required"
            return $false
        }
    }

    Write-Error "Node.js not found or version too old"
    Write-Info "Please install Node.js 14+ from https://nodejs.org/"
    Write-Info "Recommended: Download the LTS version"
    exit 1
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

        $mpvPath = (Get-Command mpv.exe).Source | Split-Path
        Write-Info "MPV location: $mpvPath"
    } else {
        Write-Warning "MPV not found - required for audio playback"
        Write-Info "Install with: choco install mpv -y"
        Write-Info "Or download from: https://mpv.io/installation/"
        Write-Info ""

        $response = Read-Host "Would you like to install MPV now? (Y/n)"
        if ($response -eq "" -or $response -eq "Y" -or $response -eq "y") {
            if (Test-Command "choco") {
                Write-Info "Installing MPV via Chocolatey..."
                choco install mpv -y
                Write-Success "MPV installed"
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
}

# Main installation
function Install-LofiGirl {
    $installDir = "$env:USERPROFILE\lofigirl-terminal"

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

    # Install Node.js dependencies
    Write-Info "Installing Node.js dependencies..."
    Push-Location $installDir

    npm install
    Write-Success "Dependencies installed"

    # Build TypeScript
    Write-Info "Building TypeScript..."
    npm run build
    Write-Success "Build complete"

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
# LofiGirl Terminal Launcher (Node.js version)

$installDir = "$env:USERPROFILE\lofigirl-terminal"

if (-not (Test-Path $installDir)) {
    Write-Error "LofiGirl Terminal is not installed"
    Write-Host "Run installation script from: https://github.com/HollyTotoC/lofigirl-terminal"
    exit 1
}

# Add MPV to PATH if needed
$mpvPath = "C:\ProgramData\chocolatey\lib\mpvio.install\tools"
if (Test-Path $mpvPath) {
    $env:PATH = "$mpvPath;$env:PATH"
}

# Run lofigirl with node
Push-Location $installDir
& node dist/index.js $args
Pop-Location
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
        Add-Content -Path $PROFILE -Value "`n# LofiGirl Terminal (Node.js)"
        Add-Content -Path $PROFILE -Value $aliasLine
        Write-Success "Added alias to PowerShell profile"
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
    Write-ColorOutput Yellow "📖 For daily usage tips, see: docs/WINDOWS_WORKFLOW.md"
    Write-Host ""
}

# Main execution
try {
    Write-Header

    Find-Node
    Test-Requirements
    Install-LofiGirl
    New-Launcher
    Show-Completion

} catch {
    Write-Error "Installation failed: $_"
    Write-Host $_.ScriptStackTrace
    exit 1
}
