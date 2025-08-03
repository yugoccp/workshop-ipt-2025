# Check if Chocolatey is installed
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Chocolatey not found. Please install Chocolatey first by following the instructions at https://chocolatey.org/install"
    exit 1
} else {
    Write-Host "Chocolatey is already installed."
}

# Install required applications
Write-Host "Installing required applications..."

# Install Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found. Installing Python..."
    choco install python --version 3.12
} else {
    Write-Host "Python is already installed."
}

# Install Ollama
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "Ollama not found. Installing Ollama..."
    choco install ollama
} else {
    Write-Host "Ollama is already installed."
}

# Install Kuzu
if (-not (Get-Command kuzu -ErrorAction SilentlyContinue)) {
    Write-Host "Kuzu not found. Installing Kuzu..."
    choco install kuzu
} else {
    Write-Host "Kuzu is already installed."
}

# Install Python dependencies
Write-Host "Setting up Python environment..."
if (-not (Test-Path -Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
} else {
    Write-Host "Virtual environment already exists."
}

Write-Host "Activating virtual environment and installing dependencies..."
& .\.venv\Scripts\Activate.ps1

Write-Host "Installing Python dependencies..."
pip install -r requirements.txt

Write-Host "Installation complete."
Write-Host "Please run '.\.venv\Scripts\Activate.ps1' to activate the virtual environment."