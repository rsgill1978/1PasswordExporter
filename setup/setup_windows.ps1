# 1Password Exporter - Windows PowerShell Setup Script
# This script automates the complete setup process for Windows
# Prerequisites: Python 3.6+ and VSCode must be installed

param()

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "1Password Exporter - Windows Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir

Write-Host "`n[1/6] Checking Prerequisites..." -ForegroundColor Yellow

# Check Python
try {
    $PythonVersion = (python --version 2>&1) -replace "Python ", ""
    Write-Host "+ Python 3 found: $PythonVersion" -ForegroundColor Green
} catch {
    Write-Host "X Python 3 is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3 from https://python.org" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check pip
try {
    python -m pip --version | Out-Null
    Write-Host "+ pip found" -ForegroundColor Green
} catch {
    Write-Host "Installing pip..." -ForegroundColor Yellow
    python -m ensurepip --upgrade
}

# Check VSCode
$CodePath = Get-Command code -ErrorAction SilentlyContinue
if ($null -eq $CodePath) {
    Write-Host "! VSCode 'code' command not found in PATH" -ForegroundColor Yellow
    Write-Host "  If VSCode is installed, add it to PATH:" -ForegroundColor Yellow
    Write-Host "  Typical location: C:\Program Files\Microsoft VS Code\bin" -ForegroundColor Yellow
    Write-Host "  Continuing anyway..." -ForegroundColor Yellow
} else {
    Write-Host "+ VSCode CLI found" -ForegroundColor Green
}

Write-Host "`n[2/6] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet 2>$null
Write-Host "+ pip upgraded" -ForegroundColor Green

Write-Host "`n[3/6] Installing system dependencies..." -ForegroundColor Yellow
Write-Host "No additional system dependencies required for Windows" -ForegroundColor Gray
Write-Host "+ System dependencies checked" -ForegroundColor Green

Write-Host "`n[4/6] Installing Python development tools..." -ForegroundColor Yellow
Write-Host "Installing linting and formatting tools..." -ForegroundColor Gray
try {
    python -m pip install --user pylint flake8 black mypy --quiet 2>$null
    Write-Host "+ Development tools installed" -ForegroundColor Green
} catch {
    Write-Host "! Optional linting tools installation failed (non-critical)" -ForegroundColor Yellow
}

Write-Host "`n[5/6] Installing VSCode Extensions..." -ForegroundColor Yellow
if ($null -ne $CodePath) {
    Write-Host "Installing Python extensions..." -ForegroundColor Gray
    code --install-extension ms-python.python --force 2>$null
    code --install-extension ms-python.vscode-pylance --force 2>$null
    code --install-extension ms-python.black-formatter --force 2>$null
    code --install-extension ms-python.flake8 --force 2>$null
    code --install-extension ms-python.mypy-type-checker --force 2>$null

    Write-Host "Installing Git extensions..." -ForegroundColor Gray
    code --install-extension eamodio.gitlens --force 2>$null
    code --install-extension mhutchie.git-graph --force 2>$null
    code --install-extension donjayamanne.githistory --force 2>$null

    Write-Host "Installing Markdown extensions..." -ForegroundColor Gray
    code --install-extension yzhang.markdown-all-in-one --force 2>$null
    code --install-extension davidanson.vscode-markdownlint --force 2>$null

    Write-Host "Installing productivity extensions..." -ForegroundColor Gray
    code --install-extension aaron-bond.better-comments --force 2>$null
    code --install-extension gruntfuggly.todo-tree --force 2>$null
    code --install-extension usernamehw.errorlens --force 2>$null
    code --install-extension oderwat.indent-rainbow --force 2>$null

    Write-Host "Installing themes..." -ForegroundColor Gray
    code --install-extension pkief.material-icon-theme --force 2>$null
    code --install-extension github.github-vscode-theme --force 2>$null

    Write-Host "Installing utilities..." -ForegroundColor Gray
    code --install-extension christian-kohler.path-intellisense --force 2>$null
    code --install-extension visualstudioexptteam.vscodeintellicode --force 2>$null
    code --install-extension mechatroner.rainbow-csv --force 2>$null

    Write-Host "+ VSCode extensions installed" -ForegroundColor Green
} else {
    Write-Host "! Skipping VSCode extensions (code command not available)" -ForegroundColor Yellow
}

Write-Host "`n[6/6] Running Tests..." -ForegroundColor Yellow
Set-Location $ProjectDir
$TestResult = python 1password_exporter.py --test-all
$TestExitCode = $LASTEXITCODE

if ($TestExitCode -eq 0) {
    Write-Host "`n============================================================" -ForegroundColor Green
    Write-Host "+ SETUP COMPLETE" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "`nYou can now run the exporter:" -ForegroundColor White
    Write-Host "  python 1password_exporter.py inputs\your_file.1pux" -ForegroundColor Yellow
    Write-Host "`nOr open the project in VSCode:" -ForegroundColor White
    Write-Host "  code `"$ProjectDir`"" -ForegroundColor Yellow
    Write-Host "`nPress F5 in VSCode to run tests with the debugger" -ForegroundColor Green
    Write-Host "`nSecurity Tip: Download sdelete from Microsoft Sysinternals" -ForegroundColor Cyan
    Write-Host "https://docs.microsoft.com/en-us/sysinternals/downloads/sdelete" -ForegroundColor Cyan
    Write-Host "  sdelete -p 5 inputs\your_file.1pux outputs\exported_passwords.csv" -ForegroundColor Yellow
} else {
    Write-Host "`nX Setup completed but tests failed" -ForegroundColor Red
    Write-Host "Please check the errors above" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "`n"
Read-Host "Press Enter to exit"
