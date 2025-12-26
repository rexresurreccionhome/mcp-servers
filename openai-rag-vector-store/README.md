# OpenAI RAG Vector Store MCP Server

A Model Context Protocol (MCP) Server that implements a RAG (Retrieval-Augmented Generation) system using OpenAI's Vector Store API to persist and retrieve search query histories with semantic search capabilities.

## Features

- **Store Search Queries with Context**: Save search queries along with contextual information (including answers/results) and timestamps into OpenAI Vector Store
- **Semantic Search**: Retrieve similar past searches using vector embeddings and semantic similarity (searches across both queries and context)
- **Date Filtering**: Filter search history by date ranges
- **Persistent Storage**: All queries and context are stored in OpenAI's Vector Store for long-term persistence

## Prerequisites

- Python 3.10 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- `uv` package manager (optional, falls back to `pip`)

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd openai-rag-vector-store
   ```

2. **Run the installation script**:
   ```bash
   ./mcp-install.sh
   ```

3. **Configure your OpenAI API key**:
   - Edit the `.env` file
   - Replace `your_api_key_here` with your actual OpenAI API key

## Usage

### Development Mode

Run the MCP Server with MCP Inspector for testing:

```bash
./mcp-run-dev.sh
```

This will:
- Start the MCP Server
- Open MCP Inspector in your browser
- Allow you to test the tools interactively

### Available Tools

#### 1. `store_search_query`

Store a search query with optional context into the vector store.

**Parameters**:
- `query` (required): The search query text to store
- `context` (optional): Additional context or metadata (can include the answer/result to the query)
- `timestamp` (optional): ISO 8601 timestamp (defaults to current time)

**Example**:
```json
{
  "query": "What are the best machine learning tutorials for beginners?",
  "context": "Top beginner-friendly ML tutorials include: 1) Andrew Ng's Coursera course, 2) fast.ai's Practical Deep Learning, 3) Google's Machine Learning Crash Course. These provide hands-on experience with real-world datasets.",
  "timestamp": "2025-12-26T10:30:00Z"
}
```

#### 2. `retrieve_search_history`

Retrieve and search through stored query history.

**Parameters**:
- `search_term` (required): Query for semantic similarity search
- `limit` (optional): Maximum results to return (default: 10)
- `start_date` (optional): Filter from this date (ISO 8601)
- `end_date` (optional): Filter until this date (ISO 8601)

**Returns**: Array of results containing `file_id`, `file_content` (full stored content including Query, Context, Timestamp), `timestamp`, and `similarity_score`

**Example**:
```json
{
  "search_term": "AI learning resources",
  "limit": 5,
  "start_date": "2025-01-01",
  "end_date": "2025-12-31"
}
```

**Example Response**:
```json
{
  "success": true,
  "results": [
    {
      "file_id": "file-123",
      "file_content": "Query: What are the best ML tutorials?\nContext: Andrew Ng's course...\nTimestamp: 2025-12-26T10:30:00Z\n\nSearch query stored...",
      "timestamp": "2025-12-26T10:30:00Z",
      "similarity_score": 0.95
    }
  ],
  "count": 1,
  "message": "Retrieved 1 search queries matching 'AI learning resources'"
}
```

## Configuration for Claude Desktop

Add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "openai-rag-vector-store": {
      "command": "/Users/YOUR_USERNAME/Desktop/projects/mcp-servers/openai-rag-vector-store/.venv/bin/python",
      "args": [
        "-m",
        "openai_rag_vector_store.main"
      ],
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}
```

## Project Structure

```
openai-rag-vector-store/
├── openai_rag_vector_store/
│   ├── __init__.py          # Package initialization
│   └── main.py              # Main MCP Server implementation
├── prompts/
│   └── create-mcp-server.md # Project specification
├── .env                      # Environment variables (API key)
├── pyproject.toml           # Project dependencies
├── mcp-install.sh           # Installation script
├── mcp-run-dev.sh           # Development mode script
└── README.md                # This file
```

## How It Works

1. **Storage**: When you store a query with context, the combined content is converted to vector embeddings using OpenAI's `text-embedding-3-small` model and saved to a persistent Vector Store
2. **Retrieval**: When searching, the search term is also converted to embeddings, and cosine similarity is calculated to find the most relevant past queries
3. **Enhanced Search**: Storing context (including answers) alongside queries enriches the vector embeddings, enabling semantic search for better retrieval accuracy
4. **Persistence**: All data is stored in OpenAI's cloud, so it persists across server restarts

## Technical Details

- **Vector Store**: Uses OpenAI's Beta Vector Store API
- **Embeddings Model**: `text-embedding-3-small` for efficient semantic search
- **Similarity Metric**: Cosine similarity for ranking results
- **Storage Format**: Documents with query, context, and timestamp

## Troubleshooting

### API Key Error
If you see "OPENAI_API_KEY not found", ensure:
1. `.env` file exists in the project root
2. It contains `OPENAI_API_KEY=your_actual_key`
3. The key is valid and active

### Installation Issues
If installation fails:
```bash
# Try with pip directly
source .venv/bin/activate
pip install -e .
```

### Vector Store Errors
The server automatically creates a vector store named `search-history-vector-store`. If you encounter issues, check your OpenAI account's vector store quota.

## Development

To modify the server:
1. Edit `openai_rag_vector_store/main.py`
2. Reinstall: `pip install -e .`
3. Test with: `./mcp-run-dev.sh`

## License

MIT

## Support

For issues or questions, please refer to the [MCP documentation](https://modelcontextprotocol.io) or OpenAI's [Vector Store API documentation](https://platform.openai.com/docs/assistants/tools/file-search).
