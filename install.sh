#!/bin/bash
# LofiGirl Terminal - Installation Script
# Usage: curl -sSL https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install.sh | bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/HollyTotoC/lofigirl-terminal.git"
INSTALL_DIR="$HOME/.lofigirl-terminal"
BIN_DIR="$HOME/.local/bin"
VENV_DIR="$INSTALL_DIR/venv"

# Print colored output
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_header() {
    echo -e "${CYAN}"
    echo "╔════════════════════════════════════════════╗"
    echo "║   🎵 LofiGirl Terminal Installer 🎵       ║"
    echo "║   Terminal Lofi Radio Player              ║"
    echo "╚════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check system requirements
check_requirements() {
    print_info "Checking system requirements..."

    # Check Python
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python found: $PYTHON_VERSION"
    else
        print_error "Python 3 is not installed"
        print_info "Install Python 3.8+ from: https://www.python.org/"
        exit 1
    fi

    # Check Git
    if command_exists git; then
        print_success "Git found"
    else
        print_error "Git is not installed"
        print_info "Install with: sudo apt install git (Ubuntu/Debian)"
        exit 1
    fi

    # Check mpv (warn if missing)
    if command_exists mpv; then
        print_success "MPV found"
    else
        print_warning "MPV not found - required for audio playback"
        print_info "Install with:"
        print_info "  Ubuntu/Debian: sudo apt install mpv"
        print_info "  macOS: brew install mpv"
        print_info "  Windows: choco install mpv"
        echo ""
        read -p "Continue without MPV? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi

    # Check yt-dlp (will be installed via pip if missing)
    if command_exists yt-dlp; then
        print_success "yt-dlp found"
    else
        print_warning "yt-dlp not found - will be installed"
    fi
}

# Create directories
create_directories() {
    print_info "Creating directories..."

    mkdir -p "$BIN_DIR"
    mkdir -p "$INSTALL_DIR"

    print_success "Directories created"
}

# Clone or update repository
install_repository() {
    print_info "Installing LofiGirl Terminal..."

    if [ -d "$INSTALL_DIR/.git" ]; then
        print_info "Repository exists, updating..."
        cd "$INSTALL_DIR"
        git fetch origin
        git reset --hard origin/main
        print_success "Repository updated"
    else
        print_info "Cloning repository..."
        rm -rf "$INSTALL_DIR"
        git clone "$REPO_URL" "$INSTALL_DIR"
        print_success "Repository cloned"
    fi
}

# Create virtual environment
create_venv() {
    print_info "Creating virtual environment..."

    cd "$INSTALL_DIR"

    if [ -d "$VENV_DIR" ]; then
        print_info "Removing old virtual environment..."
        rm -rf "$VENV_DIR"
    fi

    python3 -m venv "$VENV_DIR"
    print_success "Virtual environment created"
}

# Install dependencies
install_dependencies() {
    print_info "Installing dependencies..."

    cd "$INSTALL_DIR"
    source "$VENV_DIR/bin/activate"

    # Upgrade pip
    pip install --upgrade pip setuptools wheel --quiet

    # Install requirements
    pip install -r requirements/base.txt --quiet

    # Install package in editable mode
    pip install -e . --quiet

    print_success "Dependencies installed"
}

# Create launcher script
create_launcher() {
    print_info "Creating launcher script..."

    LAUNCHER="$BIN_DIR/lofigirl"

    cat > "$LAUNCHER" << 'EOF'
#!/bin/bash
# LofiGirl Terminal Launcher

INSTALL_DIR="$HOME/.lofigirl-terminal"
VENV_DIR="$INSTALL_DIR/venv"

# Check if installation exists
if [ ! -d "$INSTALL_DIR" ]; then
    echo "Error: LofiGirl Terminal is not installed"
    echo "Run: curl -sSL https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install.sh | bash"
    exit 1
fi

# Activate virtual environment and run
source "$VENV_DIR/bin/activate"
exec python -m lofigirl_terminal.main "$@"
EOF

    chmod +x "$LAUNCHER"
    print_success "Launcher created at $LAUNCHER"
}

# Add to PATH
add_to_path() {
    print_info "Configuring PATH..."

    # Check which shell
    SHELL_RC=""
    if [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    fi

    # Add to PATH if not already there
    if [ -n "$SHELL_RC" ] && [ -f "$SHELL_RC" ]; then
        if ! grep -q "$BIN_DIR" "$SHELL_RC"; then
            echo "" >> "$SHELL_RC"
            echo "# LofiGirl Terminal" >> "$SHELL_RC"
            echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_RC"
            print_success "Added to PATH in $SHELL_RC"
        else
            print_success "PATH already configured"
        fi
    fi
}

# Verify installation
verify_installation() {
    print_info "Verifying installation..."

    if [ -f "$BIN_DIR/lofigirl" ] && [ -x "$BIN_DIR/lofigirl" ]; then
        print_success "Installation verified"
        return 0
    else
        print_error "Installation verification failed"
        return 1
    fi
}

# Print success message
print_completion() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     🎉 Installation Complete! 🎉          ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
    echo ""
    print_success "LofiGirl Terminal installed successfully!"
    echo ""
    print_info "Quick Start:"
    echo -e "  ${CYAN}lofigirl tui${NC}        - Launch interactive TUI (recommended)"
    echo -e "  ${CYAN}lofigirl list${NC}       - List available stations"
    echo -e "  ${CYAN}lofigirl play${NC}       - Play default station"
    echo -e "  ${CYAN}lofigirl --help${NC}     - Show all commands"
    echo ""
    print_warning "Note: You may need to restart your terminal or run:"
    echo -e "  ${CYAN}source ~/.bashrc${NC}  (or ~/.zshrc)"
    echo ""
    print_info "To uninstall, run:"
    echo -e "  ${CYAN}bash ~/.lofigirl-terminal/uninstall.sh${NC}"
    echo ""
}

# Main installation process
main() {
    print_header

    check_requirements
    create_directories
    install_repository
    create_venv
    install_dependencies
    create_launcher
    add_to_path

    if verify_installation; then
        print_completion
    else
        print_error "Installation failed"
        exit 1
    fi
}

# Run main
main
