# Prompt: Add Note Creation Tool to Notes Organizer MCP Server

## Overview

This enhancement adds a note creation capability to the notes-organizer MCP Server, enabling users to create, store, and later retrieve notes through LLM interactions. Users will be able to provide a title, content, and optional overview to create well-formatted Markdown files that can be referenced in future conversations. The tool validates input parameters, sanitizes filenames, and stores notes in a centralized location for easy access and summarization by the LLM.

## Tasks

1. Using the FastMCP library, add a new tool called `add_note` to the notes-organizer MCP Server.
2. The tool must accept the following parameters:
   - `title` (required, string): The title of the note
   - `content` (required, string): The main content of the note
   - `overview` (optional, string): A brief overview or summary of the note
3. The tool will create a new Markdown file inside the `notes/` folder.
4. If the `overview` parameter is not provided by the user, automatically generate it by extracting the first 255 characters from the `content` parameter. This ensures the `get_notes` tool can properly display note summaries.
5. Generate the filename from the title by:
   - Removing special characters (keep only alphanumeric characters, spaces, hyphens, and underscores)
   - Replacing spaces with hyphens
   - Converting to a URL-friendly format (e.g., "Hello World!" becomes "Hello-World.md")
6. Structure the Markdown file to be both human-readable and LLM-friendly using the following format:
   ```markdown
   # [Title]
   [Overview if provided]
   
   ## Content
   [Content]
   ```
7. Implement validation for all parameters:
   - `title`: Must be provided and cannot exceed 100 characters
   - `content`: Must be provided and cannot exceed 1MB in size
   - `overview`: If provided, cannot exceed 255 characters
8. Return appropriate error messages for validation failures.
9. Return a success message with the created file path when the note is successfully created.
10. Handle edge cases such as:
   - Duplicate filenames (append a numeric suffix if needed)
   - Invalid characters in the title
   - File system errors

## Example

**Input:**
- Title: "Hello World!"
- Overview: "This is an overview"
- Content: "This is the content"

**Output File:** `notes/Hello-World.md`
```markdown
# Hello World!
This is an overview

## Content
This is the content
```

## Technical Requirements

- Use FastMCP framework
- Tool name: `add_note`
- File location: `notes/` directory (relative to the MCP server root)
- File format: Markdown (.md)
- Character encoding: UTF-8

## Acceptance Criteria

**AC1: Tool is exposed**  
Given: The notes-organizer MCP Server is running  
When: The user opens the MCP Server Inspector  
Then: The tool `add_note` is available in the tools list  
And: The tool shows the required parameters (`title`, `content`) and optional parameter (`overview`)

**AC2: Note is created successfully**  
Given: The notes-organizer MCP Server is running  
When: The user requests the LLM to create a new note with a valid title and content  
Then: A new Markdown file is created in the `notes/` folder  
And: The file is properly formatted with the title as heading, optional overview, and content section  
And: The user receives a success message with the file path  
And: The note is accessible for later reference and retrieval

**AC3: Validation works correctly**  
Given: The notes-organizer MCP Server is running  
When: The user attempts to create a note with invalid parameters (e.g., title exceeding 100 characters, empty content, overview exceeding 255 characters)  
Then: The tool returns an appropriate error message  
And: No file is created

**AC4: Special characters are handled**  
Given: The notes-organizer MCP Server is running  
When: The user creates a note with special characters in the title (e.g., "My Note: 2024 @ 100%!")  
Then: The filename is sanitized appropriately (e.g., "My-Note-2024-100.md")  
And: The file is created successfully  
And: The original title is preserved in the file content

**AC5: Notes can be referenced later**  
Given: A note has been created using the `add_note` tool  
When: The user asks the LLM to retrieve or summarize notes  
Then: The LLM can access and read the created note from the `notes/` folder  
And: The LLM can provide summaries or references based on the note content
