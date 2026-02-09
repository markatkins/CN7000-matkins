#!/bin/bash
#
# install_doc_packages.sh
# Installs documentation toolchain packages:
#   - pandoc: Document converter
#   - typst: Modern typesetting system
#   - wavedrom-cli: Digital timing diagram renderer
#   - svgbob: ASCII to SVG converter
#   - graphviz: Graph visualization
#   - plantuml: UML diagram generator
#
# Usage: ./install_doc_packages.sh
#
# References:
#   https://pandoc.org/installing.html#linux
#   https://github.com/typst/typst
#   https://github.com/wavedrom/cli
#   https://github.com/ivanceras/svgbob
#   https://www.graphviz.org/download/
#   https://github.com/plantuml/plantuml/releases

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_command() {
    command -v "$1" &> /dev/null
}

# Check if running on a Debian/Ubuntu system
check_apt() {
    if ! check_command apt-get; then
        log_error "This script requires apt-get (Debian/Ubuntu). Please adapt for your distribution."
        exit 1
    fi
}

install_pandoc() {
    if check_command pandoc; then
        log_info "pandoc is already installed: $(pandoc --version | head -1)"
        return 0
    fi

    log_info "Installing pandoc..."
    sudo apt-get install -y pandoc
    log_info "pandoc installed: $(pandoc --version | head -1)"
}

install_typst() {
    if check_command typst; then
        log_info "typst is already installed: $(typst --version)"
        return 0
    fi

    log_info "Installing typst..."
    local TYPST_VERSION
    TYPST_VERSION=$(curl -s https://api.github.com/repos/typst/typst/releases/latest | grep '"tag_name"' | sed -E 's/.*"([^"]+)".*/\1/')
    
    local ARCH
    ARCH=$(uname -m)
    local TYPST_ARCHIVE="typst-${ARCH}-unknown-linux-musl.tar.xz"
    local DOWNLOAD_URL="https://github.com/typst/typst/releases/download/${TYPST_VERSION}/${TYPST_ARCHIVE}"
    
    local TEMP_DIR
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"
    
    curl -fsSL "$DOWNLOAD_URL" | tar -xJ
    sudo mv "typst-${ARCH}-unknown-linux-musl/typst" /usr/local/bin/
    
    cd - > /dev/null
    rm -rf "$TEMP_DIR"
    
    log_info "typst installed: $(typst --version)"
}

install_wavedrom_cli() {
    if check_command wavedrom-cli; then
        log_info "wavedrom-cli is already installed: $(wavedrom-cli --version 2>/dev/null || echo 'version check not supported')"
        return 0
    fi

    log_info "Installing wavedrom-cli..."
    
    if ! check_command npm; then
        log_error "npm is required to install wavedrom-cli. Please install Node.js first."
        return 1
    fi
    
    sudo npm install -g wavedrom-cli
    log_info "wavedrom-cli installed"
}

install_svgbob() {
    if check_command svgbob; then
        log_info "svgbob is already installed: $(svgbob --version 2>/dev/null || echo 'installed')"
        return 0
    fi

    log_info "Installing svgbob..."
    
    # Install Rust if not present
    if ! check_command cargo; then
        log_info "Rust/Cargo not found. Installing Rust..."
        curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
        # Source cargo environment for current session
        source "$HOME/.cargo/env"
    fi
    
    cargo install svgbob_cli
    
    # Ensure ~/.cargo/bin is in PATH hint
    if [[ ":$PATH:" != *":$HOME/.cargo/bin:"* ]]; then
        log_warn "Add ~/.cargo/bin to your PATH: export PATH=\"\$HOME/.cargo/bin:\$PATH\""
    fi
    
    log_info "svgbob installed"
}

install_graphviz() {
    if check_command dot; then
        log_info "graphviz is already installed: $(dot -V 2>&1)"
        return 0
    fi

    log_info "Installing graphviz..."
    sudo apt-get install -y graphviz
    log_info "graphviz installed: $(dot -V 2>&1)"
}

install_plantuml() {
    if check_command plantuml; then
        log_info "plantuml is already installed"
        return 0
    fi

    log_info "Installing plantuml..."
    sudo apt-get install -y plantuml
    log_info "plantuml installed"
}

main() {
    log_info "Starting documentation toolchain installation..."
    echo ""
    
    check_apt
    
    log_info "Updating package lists..."
    sudo apt-get update
    echo ""
    
    install_pandoc
    echo ""
    
    install_typst
    echo ""
    
    install_wavedrom_cli
    echo ""
    
    install_svgbob
    echo ""
    
    install_graphviz
    echo ""
    
    install_plantuml
    echo ""
    
    log_info "Installation complete!"
    echo ""
    log_info "Installed packages summary:"
    echo "  - pandoc:       $(pandoc --version 2>/dev/null | head -1 || echo 'not found')"
    echo "  - typst:        $(typst --version 2>/dev/null || echo 'not found')"
    echo "  - wavedrom-cli: $(wavedrom-cli --version 2>/dev/null || echo 'installed via npm')"
    echo "  - svgbob:       $(svgbob --version 2>/dev/null || echo 'installed via cargo')"
    echo "  - graphviz:     $(dot -V 2>&1 || echo 'not found')"
    echo "  - plantuml:     $(plantuml -version 2>/dev/null | head -1 || echo 'installed')"
}

main "$@"
