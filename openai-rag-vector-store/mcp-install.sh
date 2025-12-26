#!/bin/bash

# MCP Server Installation Script for OpenAI RAG Vector Store
# This script sets up the Python environment and installs all dependencies

set -e  # Exit on error

echo "🚀 Installing OpenAI RAG Vector Store MCP Server..."

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if uv is installed
if command -v uv &> /dev/null; then
    echo "✅ Using uv for package management"
    PACKAGE_MANAGER="uv"
else
    echo "⚠️  uv not found, using pip"
    PACKAGE_MANAGER="pip"
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
if [ "$PACKAGE_MANAGER" = "uv" ]; then
    uv pip install -e .
else
    pip install -e .
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env template file..."
    cat > .env << 'EOF'
# OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_api_key_here
EOF
    echo "⚠️  Please edit .env file and add your OpenAI API key"
else
    echo "✅ .env file already exists"
fi

# Verify installation
echo "🔍 Verifying installation..."
python -c "import openai_rag_vector_store; print(f'✅ Package version: {openai_rag_vector_store.__version__}')"

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Run ./mcp-run-dev.sh to start the MCP Server in development mode"
echo ""
