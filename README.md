# MCP Servers Collection

A collection of Model Context Protocol (MCP) servers that extend LLM capabilities with specialized tools, resources, and prompts.

## 📚 Available MCP Servers

### 1. **Baker Virtual Assistant** 🍞
A master baker assistant providing expert baking advice, recipes, and temperature conversions.

**Features:**
- Baking tips and best practices
- Temperature conversion (F to C)
- Banana Loaf recipe resource
- Expert baking guidance prompts

**Use Cases:** Learning to bake, recipe assistance, baking troubleshooting

---

### 2. **App Testing Assistant** 🧪
Helps QA testers and developers learn to write integration tests for APIs.

**Features:**
- API schema documentation resources
- Integration test examples
- Test payload generator
- Assertion validator
- Testing best practices

**Use Cases:** Onboarding QA engineers, learning API testing, standardizing test practices

---

### 3. **Notes Organizer** 📝
Organize and search personal markdown notes.

**Features:**
- Create new notes with title, content, and overview
- Search notes by content or filename
- Filter by date range
- Retrieve specific notes
- Metadata extraction

**Use Cases:** Personal knowledge management, note searching, documentation organization

---

### 4. **OpenAI RAG Vector Store** 🔍
Store and semantically search query history with contextual information using OpenAI's Vector Store API.

**Features:**
- Store search queries with context (including answers/results) and timestamps
- Semantic search using OpenAI's built-in vector search (searches across queries and context)
- Date range filtering
- Persistent cloud storage via OpenAI

**Use Cases:** Search history tracking, Q&A knowledge base, semantic query matching, research organization

---

### 5. **Hello World** 👋
Simple demonstration MCP server for learning.

**Features:**
- Basic tool examples
- Simple responses

**Use Cases:** Learning MCP basics, testing MCP setup

---

## 🚀 Quick Start

### Prerequisites

1. **Install UV** (Python package manager):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Python 3.12+** is required

### Installation

#### Option 1: Install from GitHub (Easiest)

Add servers directly from GitHub to your Claude Desktop config without cloning:

**Location of Claude Desktop config:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Add this to your config:**
```json
{
  "mcpServers": {
    "baker-virtual-assistant": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/rexresurreccionhome/mcp-servers.git#subdirectory=baker-virtual-assistant",
        "baker-virtual-assistant"
      ]
    }
  }
}
```

See `claude_desktop_config.json` in this repo for all servers.

**Restart Claude Desktop** to activate.

#### Option 2: Install from Local Clone

Clone the repository first, then reference the local path:

```bash
# Clone the repository
git clone https://github.com/rexresurreccionhome/mcp-servers.git
cd mcp-servers
```

**Add to Claude Desktop config:**
```json
{
  "mcpServers": {
    "baker-virtual-assistant": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp-servers/baker-virtual-assistant",
        "run",
        "baker-virtual-assistant"
      ]
    }
  }
}
```

Replace `/absolute/path/to/mcp-servers` with your actual path. See `claude_desktop_config_local.json` for all servers.

**Restart Claude Desktop** to activate.

#### Option 3: Development Mode

For testing and debugging:

```bash
# Navigate to any server
cd baker-virtual-assistant

# Install dependencies
uv sync

# Run in development mode (opens MCP Inspector)
./mcp-run-dev.sh
```

---

## 📖 Usage

### Configuration Files

This repository includes two example Claude Desktop configurations:

1. **`claude_desktop_config.json`** - Install from GitHub using `uvx`
   - No cloning required
   - Automatically pulls latest from GitHub
   - Best for end users

2. **`claude_desktop_config_local.json`** - Run from local clone using `uv`
   - For development
   - Faster iteration
   - Test local changes

Choose the one that fits your use case and merge it into your Claude Desktop config file.

### Using with Claude Desktop

After installation, the MCP servers will be available in Claude Desktop:

1. Open Claude Desktop
2. Look for the tool/resource icons
3. Ask Claude to use the available tools

**Example prompts:**
- *"Use the baker assistant to help me make banana bread"*
- *"Generate an integration test for creating a user with invalid email"*
- *"Search my notes for information about MCP"*

### Development Mode (MCP Inspector)

Test and debug servers using the MCP Inspector:

```bash
cd <server-directory>
./mcp-run-dev.sh
```

This opens a web interface where you can:
- View all resources, tools, and prompts
- Test tool calls with custom parameters
- See real-time responses
- Debug issues

---

## 🛠️ Project Structure

Each MCP server follows this structure:

```
server-name/
├── server_name/           # Python package
│   ├── __init__.py
│   └── main.py           # Server implementation
├── pyproject.toml        # Dependencies and metadata
├── mcp-install.sh        # Install to Claude Desktop
├── mcp-run-dev.sh        # Run in development mode
└── README.md             # Server-specific documentation
```

---

## 🔧 Development

### Creating a New MCP Server

1. **Create the directory structure:**
   ```bash
   mkdir my-server
   cd my-server
   mkdir my_server
   ```

2. **Create `pyproject.toml`:**
   ```toml
   [project]
   name = "my-server"
   version = "0.1.0"
   description = "Description of your MCP server"
   readme = "README.md"
   requires-python = ">=3.12"
   dependencies = [
       "mcp[cli]>=1.23.1",
   ]

   [project.scripts]
   my-server = "my_server.main:main"
   ```

3. **Create `my_server/main.py`:**
   ```python
   from mcp.server.fastmcp import FastMCP

   mcp = FastMCP("my-server")

   @mcp.tool()
   def my_tool() -> str:
       """Description of your tool"""
       return "Hello from my tool!"

   def main():
       """Entry point for the MCP server."""
       mcp.run()

   if __name__ == "__main__":
       main()
   ```

4. **Create `my_server/__init__.py`:**
   ```python
   """My Server MCP Server."""
   __version__ = "0.1.0"
   ```

5. **Create bash scripts:**

   `mcp-install.sh`:
   ```bash
   #!/bin/bash
   uv run mcp install my_server/main.py
   ```

   `mcp-run-dev.sh`:
   ```bash
   #!/bin/bash
   uv run mcp dev my_server/main.py
   ```

6. **Make scripts executable:**
   ```bash
   chmod +x mcp-install.sh mcp-run-dev.sh
   ```

### Testing Your Server

```bash
# Install dependencies
uv sync

# Run in development mode
./mcp-run-dev.sh

# Install to Claude Desktop
./mcp-install.sh
```

---

## 📦 Package Management with UV

All servers use [UV](https://github.com/astral-sh/uv) for fast, reliable dependency management.

### Common UV Commands

```bash
# Install dependencies
uv sync

# Add a dependency
uv add package-name

# Run a command in the environment
uv run python my_script.py

# Run MCP commands
uv run mcp dev my_server/main.py
uv run mcp install my_server/main.py
```

### Why UV?

- **Fast**: 10-100x faster than pip
- **Reliable**: Deterministic dependency resolution
- **Simple**: One tool for environments and packages
- **Modern**: Built for Python 3.12+

---

## 🔌 MCP Primitives

MCP servers expose three types of primitives:

### 1. **Resources** 📄
Static, addressable content (like files or documentation).

```python
@mcp.resource("recipe://banana-loaf")
def banana_loaf_recipe() -> str:
    """Complete recipe for baking a delicious Banana Loaf"""
    return "# Banana Loaf Recipe\n..."
```

**Use when:** You have static reference material, documentation, or data

### 2. **Tools** 🛠️
Functions that LLMs can call to perform actions.

```python
@mcp.tool()
def convert_temperature(fahrenheit: float) -> dict:
    """Convert Fahrenheit to Celsius for baking"""
    celsius = (fahrenheit - 32) * 5/9
    return {"fahrenheit": fahrenheit, "celsius": celsius}
```

**Use when:** You need dynamic functionality or actions

### 3. **Prompts** 💬
Pre-configured prompts that guide LLM behavior.

```python
@mcp.prompt()
def baker_virtual_assistant(user_input: str) -> str:
    """A master baker virtual assistant"""
    return f"You are a Master Baker...\n\nUser's Question: {user_input}"
```

**Use when:** You want to configure LLM personas or behaviors

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/my-new-server`
3. Create your MCP server following the structure above
4. Test thoroughly using MCP Inspector
5. Commit your changes: `git commit -am 'Add new MCP server'`
6. Push to the branch: `git push origin feature/my-new-server`
7. Submit a pull request

### Contribution Guidelines

- Follow the existing project structure
- Include a comprehensive README for your server
- Test with both MCP Inspector and Claude Desktop
- Use descriptive tool/resource names
- Add docstrings to all functions
- Keep dependencies minimal

---

## 📄 License

MIT License - See individual server directories for specific licenses.

---

## 🆘 Troubleshooting

### Server not showing in Claude Desktop

1. Check Claude Desktop config:
   ```bash
   # macOS
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Windows
   type %APPDATA%\Claude\claude_desktop_config.json
   ```

2. Verify the server path is correct
3. Restart Claude Desktop completely
4. Check Claude Desktop logs for errors

### "uv: command not found"

Install UV:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then restart your terminal.

### MCP Inspector not opening

1. Ensure port 5173 is available
2. Check firewall settings
3. Try running directly:
   ```bash
   uv run mcp dev my_server/main.py --port 5174
   ```

### Import errors in packages

Make sure you're running from the server's root directory:
```bash
cd baker-virtual-assistant  # Not inside baker_virtual_assistant/
./mcp-run-dev.sh
```

---

## 📚 Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [UV Documentation](https://github.com/astral-sh/uv)
- [Claude Desktop](https://claude.ai/download)

---

## 🎯 Roadmap

Future MCP servers planned:
- Database query assistant
- Git repository analyzer
- Code review helper
- Documentation generator
- API client generator

---

**Made with ❤️ using Model Context Protocol**
