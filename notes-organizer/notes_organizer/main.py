import os
from pathlib import Path
from datetime import datetime
from typing import Optional
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("notes-organizer")

# Define the notes directory (in project root, not package directory)
NOTES_DIR = Path(__file__).parent.parent / "notes"


def get_note_metadata(file_path: Path) -> dict:
    """Extract metadata from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title (first H1 heading)
    title = "Untitled"
    for line in content.split('\n'):
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    # Create overview (first 150 characters of non-heading content)
    overview = ""
    for line in content.split('\n'):
        if line.strip() and not line.startswith('#'):
            overview = line.strip()[:150]
            if len(line.strip()) > 150:
                overview += "..."
            break
    
    return {
        "file_name": file_path.name,
        "title": title,
        "overview": overview
    }


def filter_by_date(file_path: Path, start_date: Optional[str], end_date: Optional[str]) -> bool:
    """Check if file modification date is within the specified range."""
    if not start_date and not end_date:
        return True
    
    mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
    
    if start_date:
        try:
            start = datetime.fromisoformat(start_date)
            if mod_time < start:
                return False
        except ValueError:
            pass  # Invalid date format, skip filter
    
    if end_date:
        try:
            end = datetime.fromisoformat(end_date)
            if mod_time > end:
                return False
        except ValueError:
            pass  # Invalid date format, skip filter
    
    return True


def search_in_content(file_path: Path, search_term: str) -> bool:
    """Search for a term in file name or content."""
    if not search_term:
        return True
    
    search_lower = search_term.lower()
    
    # Check file name
    if search_lower in file_path.stem.lower():
        return True
    
    # Check content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            if search_lower in content:
                return True
    except Exception:
        pass
    
    return False


@mcp.tool()
def get_notes(
    search: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> dict:
    """
    Read all markdown files inside the notes folder with optional filtering.
    
    Args:
        search: Optional search term to filter by file name or content
        start_date: Optional start date filter (ISO format: YYYY-MM-DD)
        end_date: Optional end date filter (ISO format: YYYY-MM-DD)
    
    Returns:
        JSON object containing matching notes with file name, title, and overview
    """
    if not NOTES_DIR.exists():
        return {
            "success": False,
            "error": "Notes directory not found",
            "notes": []
        }
    
    results = []
    
    # Find all markdown files
    md_files = list(NOTES_DIR.glob("*.md"))
    
    for file_path in md_files:
        # Apply filters
        if not filter_by_date(file_path, start_date, end_date):
            continue
        
        if not search_in_content(file_path, search):
            continue
        
        # Get metadata
        try:
            metadata = get_note_metadata(file_path)
            
            # Add modification date
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            metadata["modified_date"] = mod_time.isoformat()
            
            results.append(metadata)
        except Exception as e:
            results.append({
                "file_name": file_path.name,
                "title": "Error reading file",
                "overview": f"Error: {str(e)}",
                "modified_date": None
            })
    
    # Sort by modification date (newest first)
    results.sort(key=lambda x: x.get("modified_date", ""), reverse=True)
    
    return {
        "success": True,
        "count": len(results),
        "notes": results
    }


@mcp.tool()
def get_note(file_name: str) -> dict:
    """
    Read a specific markdown file from the notes folder.
    
    Args:
        file_name: The name of the markdown file (e.g., "MCP.md")
    
    Returns:
        JSON object containing the full content of the file or 404 error
    """
    # Ensure the file has .md extension
    if not file_name.endswith('.md'):
        file_name += '.md'
    
    file_path = NOTES_DIR / file_name
    
    # Check if file exists
    if not file_path.exists():
        return {
            "success": False,
            "error": "404 Not Found",
            "message": f"File '{file_name}' does not exist in the notes directory"
        }
    
    # Check if path is within notes directory (security check)
    try:
        file_path.resolve().relative_to(NOTES_DIR.resolve())
    except ValueError:
        return {
            "success": False,
            "error": "403 Forbidden",
            "message": "Access denied: Path traversal detected"
        }
    
    # Read the file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get modification date
        mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
        
        return {
            "success": True,
            "file_name": file_name,
            "content": content,
            "modified_date": mod_time.isoformat(),
            "size_bytes": file_path.stat().st_size
        }
    except Exception as e:
        return {
            "success": False,
            "error": "500 Internal Server Error",
            "message": f"Error reading file: {str(e)}"
        }


def main():
    """Entry point for the notes-organizer MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
