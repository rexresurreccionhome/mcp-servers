#!/bin/bash

# MCP Server Development Mode Runner for OpenAI RAG Vector Store
# This script runs the MCP Server with MCP Inspector for testing

set -e  # Exit on error

echo "🚀 Starting OpenAI RAG Vector Store MCP Server in development mode..."

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run ./mcp-install.sh first"
    exit 1
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Check if .env file exists and has API key
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create one with your OPENAI_API_KEY"
    exit 1
fi

# Load environment variables
echo "🔐 Loading environment variables from .env..."
export $(cat .env | grep -v '^#' | xargs)

# Verify API key is set
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_api_key_here" ]; then
    echo "❌ OPENAI_API_KEY not set in .env file"
    echo "Please edit .env and add your OpenAI API key"
    exit 1
fi

echo "✅ Environment configured"
echo "📡 Starting MCP Server with Inspector..."
echo ""
echo "The MCP Inspector will open in your browser."
echo "Use it to test the following tools:"
echo "  - store_search_query: Store search queries into vector store"
echo "  - retrieve_search_history: Retrieve and search query history"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the MCP Server with Inspector
mcp dev openai_rag_vector_store/main.py
