#!/bin/bash

# Install Homebrew if not already installed
if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew is already installed."
fi

# Install required applications
echo "Installing required applications..."

# Install Python
if ! command -v python &> /dev/null; then
    echo "Python not found. Installing python@3.12..."
    brew install python@3.12
else
    echo "Python is already installed."
fi

# Install Ollama
echo "Installing Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found. Installing Ollama..."
    brew install ollama
else
    echo "Ollama is already installed."
fi

# Install Python dependencies
echo "Setting up Python environment..."
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists."
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installation complete."
echo "Please run 'source .venv/bin/activate' to activate the virtual environment."