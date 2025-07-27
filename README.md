
# GenAI Examples

This project demonstrates how to build common examples useful to demonstrate GenAI features.

## 1. Install Ollama

First, install Ollama on your system:

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

## 2. Pull Required Models

Pull the necessary models for embeddings and chat:

- Note[1]: For embedding, I've used `all-minilm`, which with 384 dimensions and 46MB size.
- Note[2]: For chat model, I've used `llama3.2` with 3b parameters and 2.0GB size, which is good enough for starters.

```bash
# Pull the embedding model
ollama pull all-minilm

# Pull the chat model
ollama pull llama3.2
```

## 3. Install Python Dependencies

Install the required Python packages:

```bash
python -m venv .venv

# macOS or Linux
source ./.venv/bin/activate

# Windows
./.venv/Scripts/Activate.ps1

pip install -r requirements.txt
```