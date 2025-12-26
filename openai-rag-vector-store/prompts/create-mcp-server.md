# Prompt: Create MCP Server for OpenAI RAG Vector Store - Search History Management

## Overview
Create an MCP Server named `openai-rag-vector-store` that implements a RAG (Retrieval-Augmented Generation) system using OpenAI's Vector Store API to persist and retrieve search query histories with semantic search capabilities.

## Technical Requirements

### 1. Project Setup
- Use **FastMCP** Python library for MCP Server implementation
- Configure `pyproject.toml` with entry point: `openai_rag_vector_store.main:main`
- Use **OpenAI Python SDK** (official `openai` library) for Vector Store integration
- Environment configuration via `.env` file containing `OPENAI_API_KEY`
- Python 3.10+ compatibility

### 2. MCP Server Structure
```
openai-rag-vector-store/
├── openai_rag_vector_store/
│   ├── __init__.py
│   └── main.py          # Main MCP Server implementation
├── .env                  # OpenAI API key storage
├── pyproject.toml
├── mcp-install.sh       # Installation script
└── mcp-run-dev.sh       # Development mode script
```

### 3. Required Tools

#### Tool 1: `store_search_query`
- **Purpose**: Store a search query and its context into OpenAI Vector Store
- **Parameters**:
  - `query` (required, string): The search query text to store
  - `context` (optional, string): Additional context or metadata about the search
  - `timestamp` (optional, string): ISO 8601 timestamp (defaults to current time)
- **Behavior**:
  - Create/update vector store in OpenAI
  - Convert query to vector embeddings using OpenAI's embedding model (e.g., `text-embedding-3-small`)
  - Store the query with metadata (timestamp, context)
  - Return confirmation with vector store ID and file/chunk ID

#### Tool 2: `retrieve_search_history`
- **Purpose**: Retrieve and search through stored query history using semantic search
- **Parameters**:
  - `search_term` (optional, string): Query to search for similar past searches
  - `limit` (optional, integer, default=10): Maximum number of results to return
  - `start_date` (optional, string): ISO 8601 date to filter results from
  - `end_date` (optional, string): ISO 8601 date to filter results until
- **Behavior**:
  - Query OpenAI Vector Store using semantic similarity search
  - Filter by date range if provided
  - Return results ranked by relevance score
  - Include query text, context, timestamp, and similarity score

### 4. OpenAI Vector Store Implementation
- Initialize OpenAI client with API key from `.env`
- Create a persistent vector store named `search-history-vector-store`
- Use OpenAI's File API to upload search queries as documents
- Implement proper error handling for API rate limits and failures
- Use `text-embedding-3-small` or `text-embedding-3-large` for embeddings

### 5. Scripts

#### `mcp-install.sh`
- Create/activate Python virtual environment
- Install dependencies from `pyproject.toml` using `uv` or `pip`
- Validate `.env` file exists or create template
- Set appropriate file permissions

#### `mcp-run-dev.sh`
- Activate virtual environment
- Load environment variables from `.env`
- Run MCP Server in development mode with verbose logging
- Enable MCP Inspector for testing

### 6. Configuration Files

#### `pyproject.toml` requirements:
```toml
[project]
name = "openai-rag-vector-store"
version = "0.1.0"
dependencies = [
    "fastmcp",
    "openai",
    "python-dotenv"
]

[project.scripts]
openai-rag-vector-store = "openai_rag_vector_store.main:main"
```

#### `.env` template:
```
OPENAI_API_KEY=your_api_key_here
```

## Acceptance Criteria

### AC1: Store Search Query
```
Given: The MCP Server is running
  And: OpenAI client is initialized with valid API key
  And: Vector store is created/accessible
When: The tool `store_search_query` is called with query="machine learning tutorials"
Then: The query is converted to embeddings using OpenAI
  And: The embeddings are stored in the vector store
  And: A success response is returned with vector store ID and document ID
  And: The query is searchable via semantic similarity
```

### AC2: Retrieve Search History - Semantic Search
```
Given: The MCP Server is running
  And: OpenAI vector store contains previously stored queries
When: The tool `retrieve_search_history` is called with search_term="AI learning"
Then: OpenAI Vector Store performs semantic similarity search
  And: Returns relevant queries ranked by similarity score
  And: Each result includes: query text, context, timestamp, similarity score
  And: Results are limited to the specified limit (default 10)
```

### AC3: Retrieve Search History - Date Filtering
```
Given: The MCP Server is running
  And: Vector store contains queries from various dates
When: The tool `retrieve_search_history` is called with start_date="2025-01-01" and end_date="2025-12-31"
Then: Only queries within the date range are returned
  And: Results are sorted by relevance and timestamp
```

### AC4: Error Handling
```
Given: The MCP Server is running
When: OpenAI API key is invalid or missing
Then: The server returns a clear error message
  And: Suggests checking .env configuration

Given: A tool is called
When: OpenAI API returns a rate limit error
Then: The error is caught and returned with retry suggestions
```

### AC5: Installation and Development Scripts
```
Given: The project is cloned to a new machine
When: `mcp-install.sh` is executed
Then: Virtual environment is created
  And: All dependencies are installed
  And: .env template is created if missing
  
Given: Installation is complete
When: `mcp-run-dev.sh` is executed
Then: MCP Server starts in development mode
  And: Both tools are registered and accessible
  And: MCP Inspector can connect to the server
```

## Additional Considerations
- Implement proper logging for debugging
- Handle vector store persistence (reuse existing vs. create new)
- Consider implementing vector store cleanup/archival strategies
- Add input validation for all tool parameters
- Include comprehensive docstrings for all functions
- Consider adding a tool to delete/clear search history
- Implement pagination for large result sets

## Testing Strategy
1. Test with MCP Inspector to verify tool registration
2. Store multiple test queries with varying content
3. Verify semantic search returns relevant results
4. Test date range filtering accuracy
5. Validate error handling with invalid API keys
6. Test script functionality on clean environment
