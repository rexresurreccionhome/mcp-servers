# Hello World MCP Server

A simple Model Context Protocol (MCP) server that demonstrates basic MCP functionality with two tools related to the classic "Hello, World!" programming concept.

## Overview

This MCP server provides two tools:
- `what_is_hello_world`: Returns an explanation of what "Hello World" means in programming
- `simple_hello_world_poem`: Returns a creative poem about the "Hello, World!" phrase

## Prerequisites

- Python 3.12 or higher
- uv (recommended) or pip for package management

## Installation

1. Clone or navigate to this directory:
```bash
cd hello-world
```

2. Install dependencies using uv:
```bash
uv pip install -e .
```

Or using pip:
```bash
pip install -e .
```

## Usage

### Adding to Claude Desktop

To use this MCP server with Claude Desktop, you need to add it to your Claude Desktop configuration:

1. Run the installation script:
```bash
./mcp-install.sh
```

This will automatically configure Claude Desktop to use this MCP server.

Alternatively, you can manually add it to your Claude Desktop config file located at:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

Add the following configuration to the `mcpServers` section:

```json
{
  "mcpServers": {
    "hello-world": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/path/to/your/mcp-servers/hello-world/main.py"
        "run",
        "main.py"
      ]
    }
  }
}
```

**Note:** Update the path in the `args` array to match your actual project location.

After adding the configuration, restart Claude Desktop for the changes to take effect.

### Running the Server (Standalone)

You can also run the server directly for testing:

```bash
python main.py
```

Or use the provided shell script:

```bash
./mcp-run-dev.sh
```

### Testing with the Client

Test the server using the provided client:

```bash
python client.py
```

Or use the shell script:

```bash
./run-client.sh
```

## Tools

### `what_is_hello_world()`

Returns a brief explanation of what "Hello World" means in programming.

**Example:**
```
"Hello World is a simple program that outputs 'Hello, World!' to demonstrate basic syntax."
```

### `simple_hello_world_poem()`

Returns a creative four-line poem about the "Hello, World!" phrase.

**Example:**
```
Hello, World! A phrase so bright,
In coding realms, it sheds its light,
A simple start, a coder's friend,
From here, the journey has no end.
```

## Project Structure

```
hello-world/
├── main.py              # MCP server implementation
├── client.py            # Test client
├── pyproject.toml       # Project dependencies
├── README.md            # This file
├── mcp-install.sh       # Installation script
├── mcp-run-dev.sh       # Development server script
└── run-client.sh        # Client test script
```

## Development

The server is built using FastMCP, which provides a simple decorator-based API for creating MCP servers.

To modify or add tools, edit `main.py` and add new functions decorated with `@mcp.tool()`.

## License

MIT

## Contributing

Feel free to submit issues or pull requests to improve this example server.
