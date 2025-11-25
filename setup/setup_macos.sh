#!/bin/bash
# 1Password Exporter - macOS Setup Script
# This script automates the complete setup process for macOS
# Prerequisites: Python 3.6+ and VSCode must be installed

set -e  # Exit on any error

echo "============================================================"
echo "1Password Exporter - macOS Setup"
echo "============================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "\n${YELLOW}[1/5] Checking Prerequisites...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python 3 found: ${PYTHON_VERSION}${NC}"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}Installing pip3...${NC}"
    python3 -m ensurepip --upgrade
fi
echo -e "${GREEN}✓ pip3 found${NC}"

# Check VSCode
if ! command -v code &> /dev/null; then
    echo -e "${YELLOW}⚠ VSCode 'code' command not found in PATH${NC}"
    echo "  To enable, open VSCode and run: Cmd+Shift+P → 'Shell Command: Install code command in PATH'"
    echo "  Continuing anyway..."
else
    echo -e "${GREEN}✓ VSCode CLI found${NC}"
fi

echo -e "\n${YELLOW}[2/5] Upgrading pip...${NC}"
python3 -m pip install --upgrade pip --quiet
echo -e "${GREEN}✓ pip upgraded${NC}"

echo -e "\n${YELLOW}[3/5] Installing Python dependencies...${NC}"
# Note: This project uses only standard library, but installing dev tools
echo "Installing development/linting tools..."
pip3 install --user --quiet pylint flake8 black mypy 2>/dev/null || {
    echo -e "${YELLOW}⚠ Optional linting tools installation failed (non-critical)${NC}"
}
echo -e "${GREEN}✓ Dependencies checked${NC}"

echo -e "\n${YELLOW}[4/5] Installing VSCode Extensions...${NC}"
if command -v code &> /dev/null; then
    # Python extensions
    code --install-extension ms-python.python --force
    code --install-extension ms-python.vscode-pylance --force
    code --install-extension ms-python.black-formatter --force
    code --install-extension ms-python.flake8 --force
    code --install-extension ms-python.mypy-type-checker --force

    # Git extensions
    code --install-extension eamodio.gitlens --force
    code --install-extension mhutchie.git-graph --force
    code --install-extension donjayamanne.githistory --force

    # Markdown
    code --install-extension yzhang.markdown-all-in-one --force
    code --install-extension davidanson.vscode-markdownlint --force

    # Productivity
    code --install-extension aaron-bond.better-comments --force
    code --install-extension gruntfuggly.todo-tree --force
    code --install-extension usernamehw.errorlens --force
    code --install-extension oderwat.indent-rainbow --force

    # Themes & Icons
    code --install-extension pkief.material-icon-theme --force
    code --install-extension github.github-vscode-theme --force

    # Utilities
    code --install-extension christian-kohler.path-intellisense --force
    code --install-extension visualstudioexptteam.vscodeintellicode --force
    code --install-extension mechatroner.rainbow-csv --force

    echo -e "${GREEN}✓ VSCode extensions installed${NC}"
else
    echo -e "${YELLOW}⚠ Skipping VSCode extensions (code command not available)${NC}"
fi

echo -e "\n${YELLOW}[5/5] Running Tests...${NC}"
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
else
    echo -e "\n${RED}✗ Setup completed but tests failed${NC}"
    echo "Please check the errors above"
    exit 1
fi
