"""
OpenAI RAG Vector Store MCP Server - Search History Management

This MCP Server implements a RAG system using OpenAI's Vector Store API
to persist and retrieve search query histories with semantic search capabilities.
"""

import os
import json
import logging
import tempfile
from datetime import datetime
from typing import Optional, List, Dict
from dotenv import load_dotenv
from openai import OpenAI
from mcp.server.fastmcp import FastMCP
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

client = OpenAI(api_key=OPENAI_API_KEY)

# Vector store configuration
VECTOR_STORE_NAME = "search-history-vector-store"
vector_store_id = None


def get_or_create_vector_store() -> str:
    """Get existing vector store or create a new one."""
    global vector_store_id
    
    if vector_store_id:
        return vector_store_id
    
    try:
        # List existing vector stores
        vector_stores = client.vector_stores.list()
        # Check if our vector store already exists
        for vs in vector_stores.data:
            if vs.name == VECTOR_STORE_NAME:
                vector_store_id = vs.id
                logger.info(f"Found existing vector store: {vector_store_id}")
                return vector_store_id
        
        # Create new vector store if it doesn't exist
        vector_store = client.vector_stores.create(
            name=VECTOR_STORE_NAME
        )
        vector_store_id = vector_store.id
        logger.info(f"Created new vector store: {vector_store_id}")
        return vector_store_id
        
    except Exception as e:
        logger.error(f"Error getting/creating vector store: {str(e)}")
        raise


def store_search_query_handler(query: str, context: Optional[str] = None, timestamp: Optional[str] = None) -> dict:
    """
    Store a search query into OpenAI Vector Store.
    
    Args:
        query: The search query text to store
        context: Additional context or metadata about the search (can include the answer/result)
        timestamp: ISO 8601 timestamp (defaults to current time)
    
    Returns:
        dict: Confirmation with vector store ID and file ID
    """
    try:
        # Get or create vector store
        vs_id = get_or_create_vector_store()
        
        # Use current timestamp if not provided
        if not timestamp:
            timestamp = datetime.utcnow().isoformat()
        
        # Create a filename with metadata (query truncated for filename limits)
        safe_query = query[:50].replace('/', '_').replace('\\', '_')
        filename = f"{timestamp}___{safe_query}.txt"
        
        # Prepare document content
        document_content = f"""Query: {query}
Context: {context or ""}
Timestamp: {timestamp}

Search query stored for semantic search and retrieval."""
        
        # Create a temporary file with the query content
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp_file:
            tmp_file.write(document_content)
            tmp_file_path = tmp_file.name
        
        try:
            # Upload file to OpenAI for use with assistants/vector stores
            with open(tmp_file_path, 'rb') as file_data:
                # Upload with the metadata-rich filename
                original_name = tmp_file_path
                renamed_path = tmp_file_path.replace(os.path.basename(tmp_file_path), filename)
                os.rename(tmp_file_path, renamed_path)
                
                with open(renamed_path, 'rb') as renamed_file:
                    file = client.files.create(
                        file=renamed_file,
                        purpose='assistants',

                    )
            
            # Add file to vector store
            vector_store_file = client.vector_stores.files.create(
                vector_store_id=vs_id,
                file_id=file.id
            )
            
            logger.info(f"Stored query '{query}' with file ID: {file.id}")
            
            return {
                "success": True,
                "message": "Search query stored successfully in OpenAI Vector Store",
                "vector_store_id": vs_id,
                "file_id": file.id,
                "query": query,
                "timestamp": timestamp
            }
            
        finally:
            # Clean up temporary files
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)
            if 'renamed_path' in locals() and os.path.exists(renamed_path):
                os.remove(renamed_path)
                
    except Exception as e:
        logger.error(f"Error storing search query: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to store search query. Please check your OpenAI API key and try again."
        }


def retrieve_search_history_handler(
    search_term: Optional[str] = None,
    limit: int = 10,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> dict:
    """
    Retrieve and search through stored query history using OpenAI Vector Store.
    
    Args:
        search_term: Query to search for similar past searches
        limit: Maximum number of results to return (default: 10)
        start_date: ISO 8601 date to filter results from
        end_date: ISO 8601 date to filter results until
    
    Returns:
        dict: Search results with file_id, file_content (full text), timestamp, and similarity scores
    """
    try:
        # Get or create vector store
        vs_id = get_or_create_vector_store()
        
        # Use vector store search API (requires search_term)
        if not search_term:
            return {
                "success": False,
                "results": [],
                "count": 0,
                "message": "search_term is required to retrieve search history"
            }
        
        try:
            # Use OpenAI's vector store search API
            search_results = client.vector_stores.search(
                vector_store_id=vs_id,
                query=search_term,
                max_num_results=limit
            )
            
            # Process search results and extract content directly
            results = []
            for result in search_results.data:
                # Extract content from search result
                file_content = ""
                if hasattr(result, 'content') and result.content:
                    for content_item in result.content:
                        if content_item.type == 'text':
                            file_content += content_item.text
                
                # Parse timestamp from content
                timestamp = ""
                
                for line in file_content.split('\n'):
                    if line.startswith('Timestamp: '):
                        timestamp = line.replace('Timestamp: ', '', 1)
                
                # Apply date filtering if specified
                if timestamp and (start_date or end_date):
                    try:
                        entry_timestamp = datetime.fromisoformat(timestamp)
                        
                        if start_date:
                            start_dt = datetime.fromisoformat(start_date)
                            if entry_timestamp < start_dt:
                                continue
                        
                        if end_date:
                            end_dt = datetime.fromisoformat(end_date)
                            if entry_timestamp > end_dt:
                                continue
                    except ValueError:
                        logger.warning(f"Invalid timestamp format: {timestamp}")
                        continue
                
                results.append({
                    "file_id": result.file_id,
                    "file_content": file_content,
                    "timestamp": timestamp,
                    "similarity_score": result.score
                })
            
            return {
                "success": True,
                "results": results,
                "count": len(results),
                "message": f"Retrieved {len(results)} search queries matching '{search_term}'"
            }
            
        except Exception as e:
            logger.error(f"Error performing vector store search: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to perform search. Error: {str(e)}"
            }
        
    except Exception as e:
        logger.error(f"Error retrieving search history: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to retrieve search history. Please check your OpenAI API key and try again."
        }


# Create FastMCP Server
mcp = FastMCP("openai-rag-vector-store")


@mcp.tool()
def store_search_query(query: str, context: str = "", timestamp: str = "") -> dict:
    """
    Store a search query and its context into OpenAI Vector Store for future retrieval.
    
    Args:
        query: The search query text to store
        context: Additional context or metadata about the search (can include the answer/result to the query)
        timestamp: ISO 8601 timestamp (defaults to current time if not provided)
    
    Returns:
        dict: Confirmation with vector store ID and file ID
    """
    return store_search_query_handler(query, context if context else None, timestamp if timestamp else None)


@mcp.tool()
def retrieve_search_history(
    search_term: str,
    limit: int = 10,
    start_date: str = "",
    end_date: str = ""
) -> dict:
    """
    Retrieve and search through stored query history using semantic search with optional date filtering.
    
    Args:
        search_term: Query to search for similar past searches using semantic similarity (required)
        limit: Maximum number of results to return (default: 10)
        start_date: ISO 8601 date to filter results from (e.g., '2025-01-01')
        end_date: ISO 8601 date to filter results until (e.g., '2025-12-31')
    
    Returns:
        dict: Search results with file_id, file_content (includes Query, Context, Timestamp), and similarity_score for each result
    """
    return retrieve_search_history_handler(
        search_term,
        limit,
        start_date if start_date else None,
        end_date if end_date else None
    )


def main():
    """Main entry point for the MCP Server."""
    logger.info("Starting OpenAI RAG Vector Store MCP Server...")
    
    # Initialize vector store on startup
    try:
        vs_id = get_or_create_vector_store()
        logger.info(f"Vector store ready: {vs_id}")
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {str(e)}")
        logger.error("Server will continue but may not function properly.")
    
    # Run the FastMCP server
    mcp.run()


if __name__ == "__main__":
    main()
