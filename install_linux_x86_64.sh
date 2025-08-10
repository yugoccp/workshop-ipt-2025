#!/bin/bash

# Update package list and install dependencies
echo "Updating package list and installing dependencies..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv curl

# Install Ollama
if ! command -v ollama &> /dev/null; then
    echo "Ollama not found. Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "Ollama is already installed."
fi

# Install Kuzu
if ! command -v kuzu &> /dev/null; then
    echo "Kuzu not found. Installing Kuzu..."
    curl -L -O https://github.com/kuzudb/kuzu/releases/download/v0.11.1/kuzu_cli-linux-x86_64.tar.gz
    tar xzf kuzu_cli-*.tar.gz
else
    echo "Kuzu is already installed."
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
