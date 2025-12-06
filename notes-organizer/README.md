# Notes Organizer MCP Server

An MCP (Model Context Protocol) server for organizing and searching through personal markdown notes using FastMCP.

## Features

- **Search and filter notes** by content, filename, and modification date
- **Read individual notes** with full content retrieval
- **Semi-structured JSON responses** for easy integration
- **Date range filtering** for time-based note discovery

## Tools

### 1. `get_notes`
Read all markdown files in the notes folder with optional filtering.

**Parameters:**
- `search` (optional): Search term to filter by file name or content
- `start_date` (optional): Start date filter in ISO format (YYYY-MM-DD)
- `end_date` (optional): End date filter in ISO format (YYYY-MM-DD)

**Returns:**
```json
{
  "success": true,
  "count": 1,
  "notes": [
    {
      "file_name": "MCP.md",
      "title": "About MCP",
      "overview": "Model Context Protocol (MCP) - Is a standard (protocol) for AI...",
      "modified_date": "2024-12-06T10:30:00"
    }
  ]
}
```

### 2. `get_note`
Read a specific markdown file from the notes folder.

**Parameters:**
- `file_name` (required): The name of the markdown file (e.g., "MCP.md")

**Returns:**
```json
{
  "success": true,
  "file_name": "MCP.md",
  "content": "# About MCP\n\n## MCP\n\n...",
  "modified_date": "2024-12-06T10:30:00",
  "size_bytes": 1234
}
```

**Error Response (404):**
```json
{
  "success": false,
  "error": "404 Not Found",
  "message": "File 'nonexistent.md' does not exist in the notes directory"
}
```

## Installation

1. Clone or navigate to the project directory
2. Install the package:
```bash
pip install -e .
```

## Usage

### Running the Server

```bash
python main.py
```

Or use the MCP CLI:
```bash
mcp run main.py
```

### Testing the Tools

You can test the tools by connecting an MCP client (like Claude Desktop) to this server.

#### Configuration for Claude Desktop

Add to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "notes-organizer": {
      "command": "python",
      "args": ["/path/to/notes-organizer/main.py"]
    }
  }
}
```

## Directory Structure

```
notes-organizer/
├── main.py                 # MCP server implementation
├── pyproject.toml          # Project dependencies
├── README.md               # This file
└── notes/                  # Directory containing markdown notes
    └── *.md               # Your markdown notes
```

## Examples

### Search for notes containing "MCP"
```python
get_notes(search="MCP")
```

### Get notes modified in December 2024
```python
get_notes(start_date="2024-12-01", end_date="2024-12-31")
```

### Read a specific note
```python
get_note(file_name="MCP.md")
```

## Security Features

- Path traversal protection prevents accessing files outside the notes directory
- File extension validation ensures only markdown files are accessed
- Graceful error handling for missing or inaccessible files

## Requirements

- Python >= 3.12
- mcp[cli] >= 1.23.1

## License

MIT
