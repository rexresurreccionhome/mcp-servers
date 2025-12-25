#!/bin/bash

# Run the OpenAI-integrated MCP client for baker-virtual-assistant
# This script requires a .env file with OPENAI_API_KEY configured

echo "Running OpenAI-Integrated Baker Virtual Assistant Client..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo ""
    echo "Please create a .env file with your OpenAI API key."
    echo "You can copy .env.example and add your API key:"
    echo ""
    echo "  cp .env.example .env"
    echo "  # Then edit .env and add your OpenAI API key"
    echo ""
    exit 1
fi

# Run the client using uv
uv run client_openai.py
