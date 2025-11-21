#!/bin/bash
# LofiGirl Terminal - Uninstallation Script
# Usage: bash ~/.lofigirl-terminal/uninstall.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="$HOME/.lofigirl-terminal"
BIN_DIR="$HOME/.local/bin"
LAUNCHER="$BIN_DIR/lofigirl"

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
    echo "║   🗑️  LofiGirl Terminal Uninstaller       ║"
    echo "╚════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Confirm uninstallation
confirm_uninstall() {
    echo ""
    print_warning "This will remove LofiGirl Terminal completely from your system."
    echo ""
    print_info "The following will be deleted:"
    echo "  - Installation directory: $INSTALL_DIR"
    echo "  - Launcher script: $LAUNCHER"
    echo "  - Configuration files: ~/.config/lofigirl (if exists)"
    echo ""
    read -p "Are you sure you want to continue? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Uninstallation cancelled"
        exit 0
    fi
}

# Remove launcher
remove_launcher() {
    if [ -f "$LAUNCHER" ]; then
        print_info "Removing launcher..."
        rm -f "$LAUNCHER"
        print_success "Launcher removed"
    fi
}

# Remove installation directory
remove_installation() {
    if [ -d "$INSTALL_DIR" ]; then
        print_info "Removing installation directory..."
        rm -rf "$INSTALL_DIR"
        print_success "Installation directory removed"
    fi
}

# Remove configuration
remove_config() {
    CONFIG_DIR="$HOME/.config/lofigirl"
    if [ -d "$CONFIG_DIR" ]; then
        print_info "Removing configuration..."
        read -p "Remove configuration files? (y/N) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$CONFIG_DIR"
            print_success "Configuration removed"
        else
            print_info "Configuration kept"
        fi
    fi
}

# Clean PATH (optional)
clean_path() {
    print_info "Cleaning PATH entries..."

    SHELL_RC=""
    if [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    fi

    if [ -n "$SHELL_RC" ] && [ -f "$SHELL_RC" ]; then
        # Check if we added PATH entry
        if grep -q "# LofiGirl Terminal" "$SHELL_RC"; then
            read -p "Remove PATH entry from $SHELL_RC? (y/N) " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                # Remove our lines
                sed -i '/# LofiGirl Terminal/,+1d' "$SHELL_RC" 2>/dev/null || \
                sed -i '' '/# LofiGirl Terminal/,+1d' "$SHELL_RC" 2>/dev/null
                print_success "PATH entry removed"
            fi
        fi
    fi
}

# Verify uninstallation
verify_uninstall() {
    print_info "Verifying uninstallation..."

    local all_clean=true

    if [ -d "$INSTALL_DIR" ]; then
        print_warning "Installation directory still exists"
        all_clean=false
    fi

    if [ -f "$LAUNCHER" ]; then
        print_warning "Launcher script still exists"
        all_clean=false
    fi

    if [ "$all_clean" = true ]; then
        print_success "Uninstallation complete"
        return 0
    else
        print_error "Some files could not be removed"
        return 1
    fi
}

# Print completion message
print_completion() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     👋 Uninstallation Complete            ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
    echo ""
    print_success "LofiGirl Terminal has been removed from your system"
    echo ""
    print_info "To reinstall, run:"
    echo -e "  ${CYAN}curl -sSL https://raw.githubusercontent.com/HollyTotoC/lofigirl-terminal/main/install.sh | bash${NC}"
    echo ""
    print_info "Thank you for using LofiGirl Terminal! 🎵"
    echo ""
}

# Main uninstallation process
main() {
    print_header

    # Check if installed
    if [ ! -d "$INSTALL_DIR" ] && [ ! -f "$LAUNCHER" ]; then
        print_warning "LofiGirl Terminal does not appear to be installed"
        exit 0
    fi

    confirm_uninstall
    remove_launcher
    remove_installation
    remove_config
    clean_path

    if verify_uninstall; then
        print_completion
    else
        print_error "Uninstallation completed with warnings"
        exit 1
    fi
}

# Run main
main
