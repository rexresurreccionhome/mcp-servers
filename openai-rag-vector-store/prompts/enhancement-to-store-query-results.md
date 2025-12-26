# Prompt: Enhanced MCP Server with Contextual Storage

## Context
The `openai-rag-vector-store` MCP Server stores search queries with contextual information in OpenAI's Vector Store, enabling semantic search and retrieval of historical queries with their associated context (including answers/results).

**Current Implementation:**
- File: `/Users/rresurreccion/Desktop/projects/mcp-servers/openai-rag-vector-store/openai_rag_vector_store/main.py`
- Tools: `store_search_query`, `retrieve_search_history`
- Storage format: Query + Context + Timestamp

## Objective
The MCP Server stores queries with contextual information, enabling Q&A history tracking and improved semantic search across both questions and contextual answers.

## Requirements

### 1. `store_search_query_handler` Function
- Accepts `query`, `context`, and `timestamp` parameters
- `context` parameter is optional and can include answers/results or any other metadata
- Document content format:
  ```
  Query: {query}
  Context: {context or ""}
  Timestamp: {timestamp}
  ```

### 2. `store_search_query` MCP Tool
- Parameters: `query` (required), `context` (optional), `timestamp` (optional)
- Context can include the answer/result to the query
- Passes all parameters to `store_search_query_handler`

### 3. `retrieve_search_history_handler` Function
- Uses OpenAI's vector store search API
- Extracts full content from search results
- Returns structure includes `file_id`, `file_content`, `timestamp`, and `similarity_score`
- Performs semantic search and date filtering

### 4. Documentation
- All docstrings clarify that `context` can include answers/results
- Success messages reflect contextual storage

## Expected Behavior

**Storing with context:**
```python
store_search_query(
    query="What is the capital of France?",
    context="The capital of France is Paris, located in the north-central part of the country.",
    timestamp="2025-12-26T10:30:00"
)
```

**Retrieving with context:**
```python
retrieve_search_history(search_term="France capital", limit=5)
# Returns:
{
    "success": True,
    "results": [
        {
            "file_id": "file-123",
            "file_content": "Query: What is the capital of France?\nContext: The capital of France is Paris, located in the north-central part of the country.\nTimestamp: 2025-12-26T10:30:00\n\nSearch query stored for semantic search and retrieval.",
            "timestamp": "2025-12-26T10:30:00",
            "similarity_score": 0.95
        }
    ],
    "count": 1,
    "message": "Retrieved 1 search queries matching 'France capital'"
}
```

## Implementation Notes
- The `context` field can include answers, results, or any additional metadata
- Storing context enriches vector embeddings, improving semantic search quality
- Semantic search works across both query and context for better retrieval
- Simple, flexible API with just query, context, and timestamp
