#!/bin/bash
# Quick setup script for the project

echo "🚀 Setting up LangGraph Multi-Agent System..."
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed"
    echo "Please install uv: https://github.com/astral-sh/uv"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
uv venv

# Activate (show instructions)
echo ""
echo "✅ Virtual environment created!"
echo ""
echo "To activate it, run:"
echo "  source .venv/bin/activate"
echo ""

# Check if activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Please activate the virtual environment first:"
    echo "   source .venv/bin/activate"
    echo ""
    echo "Then run this script again."
    exit 0
fi

# Install dependencies
echo "📥 Installing dependencies..."
uv pip install -e .

# Check .env file
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  No .env file found"
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env and add your TAVILY_API_KEY"
fi

# Check Ollama
echo ""
echo "🔍 Checking Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed"
    echo "Please install: https://ollama.com"
else
    echo "✅ Ollama is installed"
    
    # Check if mistral is pulled
    if ollama list | grep -q mistral; then
        echo "✅ Mistral model is available"
    else
        echo "📥 Pulling Mistral model..."
        ollama pull mistral
    fi
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Add your TAVILY_API_KEY to .env"
echo "  2. Run: python examples/interactive_cli.py"
echo ""