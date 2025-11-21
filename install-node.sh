#!/usr/bin/env bash
# LofiGirl Terminal - Installation Script (Node.js version)
# Compatible with Linux and macOS
# Usage: curl -sSL https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install-node.sh | bash

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

success() {
    echo -e "${GREEN}✓ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}✗ $1${NC}"
}

header() {
    echo -e "${CYAN}"
    cat << "EOF"

╔════════════════════════════════════════════╗
║   🎵 LofiGirl Terminal Installer 🎵       ║
║   Cross-Platform Lofi Radio Player        ║
║   (Node.js/TypeScript Edition)            ║
╚════════════════════════════════════════════╝

EOF
    echo -e "${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Find Node.js installation
find_node() {
    info "Detecting Node.js installation..."

    if command_exists node; then
        NODE_VERSION=$(node --version)
        NPM_VERSION=$(npm --version)
        MAJOR_VERSION=$(echo "$NODE_VERSION" | sed 's/v\([0-9]*\).*/\1/')

        if [ "$MAJOR_VERSION" -ge 14 ]; then
            success "Found Node.js: $NODE_VERSION (npm: $NPM_VERSION)"
            return 0
        else
            warning "Node.js version $NODE_VERSION found but v14+ required"
            return 1
        fi
    fi

    error "Node.js not found or version too old"
    echo ""
    info "Please install Node.js 14+ from:"
    echo "  - macOS: brew install node"
    echo "  - Ubuntu/Debian: sudo apt install nodejs npm"
    echo "  - Fedora: sudo dnf install nodejs npm"
    echo "  - Or download from: https://nodejs.org/"
    exit 1
}

# Check system requirements
check_requirements() {
    info "Checking system requirements..."

    # Check Git
    if command_exists git; then
        GIT_VERSION=$(git --version)
        success "Git found: $GIT_VERSION"
    else
        error "Git is not installed"
        info "Install with:"
        echo "  - macOS: brew install git"
        echo "  - Ubuntu/Debian: sudo apt install git"
        echo "  - Fedora: sudo dnf install git"
        exit 1
    fi

    # Check MPV
    if command_exists mpv; then
        MPV_VERSION=$(mpv --version | head -n1)
        success "MPV found: $MPV_VERSION"
    else
        warning "MPV not found - required for audio playback"
        echo ""
        info "Install with:"
        echo "  - macOS: brew install mpv"
        echo "  - Ubuntu/Debian: sudo apt install mpv"
        echo "  - Fedora: sudo dnf install mpv"
        echo ""
        read -p "Continue without MPV? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Install LofiGirl Terminal
install_lofigirl() {
    INSTALL_DIR="$HOME/.lofigirl-terminal"

    info "Installing LofiGirl Terminal to: $INSTALL_DIR"

    # Clone or update repository
    if [ -d "$INSTALL_DIR/.git" ]; then
        info "Repository exists, updating..."
        cd "$INSTALL_DIR"
        git fetch origin
        git reset --hard origin/main
        success "Repository updated"
    else
        info "Cloning repository..."
        if [ -d "$INSTALL_DIR" ]; then
            rm -rf "$INSTALL_DIR"
        fi
        git clone "https://github.com/HollyTotoC/lofigirl-terminal.git" "$INSTALL_DIR"
        success "Repository cloned"
    fi

    # Install Node.js dependencies
    info "Installing Node.js dependencies..."
    cd "$INSTALL_DIR"
    npm install
    success "Dependencies installed"

    # Build TypeScript
    info "Building TypeScript..."
    npm run build
    success "Build complete"
}

# Create launcher script
create_launcher() {
    BIN_DIR="$HOME/.local/bin"
    LAUNCHER_PATH="$BIN_DIR/lofigirl"

    # Create bin directory if it doesn't exist
    if [ ! -d "$BIN_DIR" ]; then
        mkdir -p "$BIN_DIR"
    fi

    # Create launcher script
    cat > "$LAUNCHER_PATH" << 'EOF'
#!/usr/bin/env bash
# LofiGirl Terminal Launcher (Node.js version)

INSTALL_DIR="$HOME/.lofigirl-terminal"

if [ ! -d "$INSTALL_DIR" ]; then
    echo "Error: LofiGirl Terminal is not installed"
    echo "Run installation script from: https://github.com/HollyTotoC/lofigirl-terminal"
    exit 1
fi

# Run lofigirl with node
cd "$INSTALL_DIR"
node dist/index.js "$@"
EOF

    chmod +x "$LAUNCHER_PATH"
    success "Launcher created at: $LAUNCHER_PATH"

    # Add to PATH if needed
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        info "Adding $BIN_DIR to PATH..."

        # Detect shell and add to appropriate config
        SHELL_NAME=$(basename "$SHELL")
        case "$SHELL_NAME" in
            bash)
                SHELL_CONFIG="$HOME/.bashrc"
                ;;
            zsh)
                SHELL_CONFIG="$HOME/.zshrc"
                ;;
            fish)
                SHELL_CONFIG="$HOME/.config/fish/config.fish"
                ;;
            *)
                SHELL_CONFIG="$HOME/.profile"
                ;;
        esac

        if ! grep -q "$BIN_DIR" "$SHELL_CONFIG" 2>/dev/null; then
            echo "" >> "$SHELL_CONFIG"
            echo "# LofiGirl Terminal (Node.js)" >> "$SHELL_CONFIG"
            echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_CONFIG"
            success "Added to $SHELL_CONFIG"
            warning "Restart your shell or run: source $SHELL_CONFIG"
        fi
    else
        success "$BIN_DIR is already in PATH"
    fi
}

# Print completion message
show_completion() {
    echo ""
    echo -e "${GREEN}"
    cat << "EOF"
╔════════════════════════════════════════════╗
║     🎉 Installation Complete! 🎉          ║
╚════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    success "LofiGirl Terminal installed successfully!"
    echo ""
    info "Quick Start:"
    echo -e "${CYAN}  lofigirl tui        - Launch interactive TUI (recommended)${NC}"
    echo -e "${CYAN}  lofigirl list       - List available stations${NC}"
    echo -e "${CYAN}  lofigirl play       - Play default station${NC}"
    echo -e "${CYAN}  lofigirl --help     - Show all commands${NC}"
    echo ""
    warning "Note: Restart your shell or run:"
    echo -e "${CYAN}  source ~/.bashrc    # or ~/.zshrc${NC}"
    echo ""
    info "To uninstall, run:"
    echo -e "${CYAN}  rm -rf ~/.lofigirl-terminal ~/.local/bin/lofigirl${NC}"
    echo ""
}

# Main execution
main() {
    header
    find_node
    check_requirements
    install_lofigirl
    create_launcher
    show_completion
}

# Run main function
main
