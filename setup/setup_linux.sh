#!/bin/bash
# 1Password Exporter - Linux Mint Setup Script
# This script automates the complete setup process for Linux Mint (and compatible Ubuntu-based distros)
# Prerequisites: Python 3.6+ and VSCode must be installed

set -e  # Exit on any error

echo "============================================================"
echo "1Password Exporter - Linux Mint Setup"
echo "============================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "\n${YELLOW}[1/6] Checking Prerequisites...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    echo "Please install Python 3: sudo apt install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python 3 found: ${PYTHON_VERSION}${NC}"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}Installing pip3...${NC}"
    sudo apt update
    sudo apt install -y python3-pip
fi
echo -e "${GREEN}✓ pip3 found${NC}"

# Check VSCode
if ! command -v code &> /dev/null; then
    echo -e "${YELLOW}⚠ VSCode 'code' command not found in PATH${NC}"
    echo "  If VSCode is installed, try: export PATH=\"\$PATH:/usr/share/code/bin\""
    echo "  Continuing anyway..."
else
    echo -e "${GREEN}✓ VSCode CLI found${NC}"
fi

echo -e "\n${YELLOW}[2/6] Upgrading pip...${NC}"
python3 -m pip install --upgrade pip --user --quiet
echo -e "${GREEN}✓ pip upgraded${NC}"

echo -e "\n${YELLOW}[3/6] Installing system dependencies...${NC}"
# Install useful tools for secure file deletion
if ! command -v shred &> /dev/null; then
    echo "Installing coreutils (includes shred)..."
    sudo apt install -y coreutils 2>/dev/null || echo -e "${YELLOW}⚠ coreutils install failed (non-critical)${NC}"
fi
echo -e "${GREEN}✓ System dependencies checked${NC}"

echo -e "\n${YELLOW}[4/6] Installing Python development tools...${NC}"
# Install development/linting tools
echo "Installing linting and formatting tools..."
pip3 install --user --quiet pylint flake8 black mypy 2>/dev/null || {
    echo -e "${YELLOW}⚠ Optional linting tools installation failed (non-critical)${NC}"
}
echo -e "${GREEN}✓ Development tools installed${NC}"

echo -e "\n${YELLOW}[5/6] Installing VSCode Extensions...${NC}"
if command -v code &> /dev/null; then
    echo "Installing Python extensions..."
    code --install-extension ms-python.python --force 2>/dev/null
    code --install-extension ms-python.vscode-pylance --force 2>/dev/null
    code --install-extension ms-python.black-formatter --force 2>/dev/null
    code --install-extension ms-python.flake8 --force 2>/dev/null
    code --install-extension ms-python.mypy-type-checker --force 2>/dev/null

    echo "Installing Git extensions..."
    code --install-extension eamodio.gitlens --force 2>/dev/null
    code --install-extension mhutchie.git-graph --force 2>/dev/null
    code --install-extension donjayamanne.githistory --force 2>/dev/null

    echo "Installing Markdown extensions..."
    code --install-extension yzhang.markdown-all-in-one --force 2>/dev/null
    code --install-extension davidanson.vscode-markdownlint --force 2>/dev/null

    echo "Installing productivity extensions..."
    code --install-extension aaron-bond.better-comments --force 2>/dev/null
    code --install-extension gruntfuggly.todo-tree --force 2>/dev/null
    code --install-extension usernamehw.errorlens --force 2>/dev/null
    code --install-extension oderwat.indent-rainbow --force 2>/dev/null

    echo "Installing themes..."
    code --install-extension pkief.material-icon-theme --force 2>/dev/null
    code --install-extension github.github-vscode-theme --force 2>/dev/null

    echo "Installing utilities..."
    code --install-extension christian-kohler.path-intellisense --force 2>/dev/null
    code --install-extension visualstudioexptteam.vscodeintellicode --force 2>/dev/null
    code --install-extension mechatroner.rainbow-csv --force 2>/dev/null

    echo -e "${GREEN}✓ VSCode extensions installed${NC}"
else
    echo -e "${YELLOW}⚠ Skipping VSCode extensions (code command not available)${NC}"
fi

echo -e "\n${YELLOW}[6/6] Running Tests...${NC}"
cd "$PROJECT_DIR"
python3 1password_exporter.py --test-all

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}============================================================${NC}"
    echo -e "${GREEN}✓ SETUP COMPLETE${NC}"
    echo -e "${GREEN}============================================================${NC}"
    echo -e "\nYou can now run the exporter:"
    echo -e "  ${YELLOW}python3 1password_exporter.py inputs/your_file.1pux${NC}"
    echo -e "\nOr open the project in VSCode:"
    echo -e "  ${YELLOW}code $PROJECT_DIR${NC}"
    echo -e "\n${GREEN}Press F5 in VSCode to run tests with the debugger${NC}"
    echo -e "\n${YELLOW}Security Tip:${NC} Use shred to securely delete files:"
    echo -e "  ${YELLOW}shred -vfz -n 5 inputs/your_file.1pux outputs/exported_passwords.csv${NC}"
else
    echo -e "\n${RED}✗ Setup completed but tests failed${NC}"
    echo "Please check the errors above"
    exit 1
fi
