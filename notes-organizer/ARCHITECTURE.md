# Notes Organizer MCP Server - Architecture

## System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Claude[Claude Desktop/AI Client]
    end
    
    subgraph "MCP Protocol"
        MCP[MCP Protocol Layer]
    end
    
    subgraph "Notes Organizer Server"
        FastMCP[FastMCP Server]
        Tools[Tool Handlers]
        Utils[Utility Functions]
    end
    
    subgraph "Storage Layer"
        NotesDir[Notes Directory]
        MarkdownFiles[Markdown Files]
    end
    
    Claude <-->|MCP Messages| MCP
    MCP <-->|Tool Calls| FastMCP
    FastMCP --> Tools
    Tools --> Utils
    Utils <-->|Read/Write| NotesDir
    NotesDir --> MarkdownFiles
```

## Tool Flow Diagram

```mermaid
flowchart TD
    Start([User Request to Claude]) --> Decision{Which Tool?}
    
    Decision -->|Create Note| AddNote[add_note]
    Decision -->|List Notes| GetNotes[get_notes]
    Decision -->|Read Note| GetNote[get_note]
    
    AddNote --> ValidateAdd{Validate Input}
    ValidateAdd -->|Invalid| ErrorAdd[Return Error]
    ValidateAdd -->|Valid| SanitizeFilename[Sanitize Filename]
    SanitizeFilename --> CheckUnique[Get Unique Filename]
    CheckUnique --> CreateFile[Create Markdown File]
    CreateFile --> SuccessAdd[Return Success + File Path]
    
    GetNotes --> CheckDir{Notes Dir Exists?}
    CheckDir -->|No| ErrorDir[Return Empty List]
    CheckDir -->|Yes| FindFiles[Find *.md Files]
    FindFiles --> FilterDate[Apply Date Filter]
    FilterDate --> FilterSearch[Apply Search Filter]
    FilterSearch --> ExtractMetadata[Extract Metadata]
    ExtractMetadata --> SortResults[Sort by Modified Date]
    SortResults --> ReturnList[Return Notes List]
    
    GetNote --> ValidateFile{File Exists?}
    ValidateFile -->|No| Error404[Return 404 Error]
    ValidateFile -->|Yes| SecurityCheck{Path Traversal Check}
    SecurityCheck -->|Unsafe| Error403[Return 403 Error]
    SecurityCheck -->|Safe| ReadContent[Read File Content]
    ReadContent --> ReturnContent[Return Full Content]
    
    ErrorAdd --> End([Response to Claude])
    SuccessAdd --> End
    ErrorDir --> End
    ReturnList --> End
    Error404 --> End
    Error403 --> End
    ReturnContent --> End
```

## Sequence Diagram - Creating a Note

```mermaid
sequenceDiagram
    participant User
    participant Claude
    participant MCP as MCP Server
    participant FS as File System
    
    User->>Claude: "Create a note about Python decorators"
    Claude->>MCP: add_note(title, content, overview)
    
    MCP->>MCP: Validate inputs (title, content, overview)
    
    alt Validation Failed
        MCP-->>Claude: {success: false, error: "Validation Error"}
        Claude-->>User: "There was a problem with the note..."
    else Validation Passed
        MCP->>MCP: Sanitize filename from title
        MCP->>MCP: Get unique filename
        MCP->>FS: Create/Write markdown file
        FS-->>MCP: File created successfully
        MCP-->>Claude: {success: true, file_path, file_name}
        Claude-->>User: "I've created your note about Python decorators"
    end
```

## Sequence Diagram - Searching Notes

```mermaid
sequenceDiagram
    participant User
    participant Claude
    participant MCP as MCP Server
    participant FS as File System
    
    User->>Claude: "Find notes about MCP from last week"
    Claude->>MCP: get_notes(search="MCP", start_date="2024-12-14")
    
    MCP->>FS: Check if notes directory exists
    
    alt Directory Not Found
        MCP-->>Claude: {success: false, notes: []}
        Claude-->>User: "No notes directory found"
    else Directory Exists
        MCP->>FS: List all *.md files
        FS-->>MCP: [file1.md, file2.md, ...]
        
        loop For each file
            MCP->>MCP: Apply date filter
            MCP->>FS: Check file modified date
            MCP->>MCP: Apply search filter
            MCP->>FS: Read file content
            MCP->>MCP: Extract metadata (title, overview)
        end
        
        MCP->>MCP: Sort results by modified date
        MCP-->>Claude: {success: true, count: 2, notes: [...]}
        Claude-->>User: "I found 2 notes about MCP from last week..."
    end
```

## Data Flow - File Structure

```mermaid
flowchart LR
    subgraph Input
        Title[Title: String]
        Content[Content: String]
        Overview[Overview?: String]
    end
    
    subgraph Processing
        Sanitize[Sanitize Title<br/>Remove special chars<br/>Replace spaces with -]
        Unique[Add counter if<br/>file exists]
        Format[Format Markdown<br/># Title<br/>Overview<br/><br/>## Content]
    end
    
    subgraph Output
        File[python-decorators.md]
        Content2[Markdown Content]
    end
    
    Title --> Sanitize
    Sanitize --> Unique
    Unique --> File
    
    Content --> Format
    Overview --> Format
    Format --> Content2
    Content2 --> File
```

## Component Breakdown

```mermaid
graph TD
    subgraph "Core Components"
        Main[main.py]
    end
    
    subgraph "Tools - User Facing"
        T1[add_note<br/>Create new note]
        T2[get_notes<br/>List/search notes]
        T3[get_note<br/>Read specific note]
    end
    
    subgraph "Utility Functions"
        U1[sanitize_filename<br/>Clean title for filename]
        U2[get_unique_filename<br/>Prevent overwrites]
        U3[get_note_metadata<br/>Extract title & overview]
        U4[filter_by_date<br/>Date range filtering]
        U5[search_in_content<br/>Text search]
    end
    
    subgraph "Data Layer"
        D1[NOTES_DIR<br/>Path to notes/]
        D2[Markdown Files<br/>.md documents]
    end
    
    Main --> T1
    Main --> T2
    Main --> T3
    
    T1 --> U1
    T1 --> U2
    T2 --> U3
    T2 --> U4
    T2 --> U5
    T3 --> D1
    
    U1 --> D1
    U2 --> D1
    U3 --> D2
    U4 --> D2
    U5 --> D2
```

## Key Design Decisions

### 1. **Filename Sanitization**
- Converts titles to safe filenames
- Removes special characters
- Replaces spaces with hyphens
- Ensures uniqueness with numeric suffixes

### 2. **Metadata Extraction**
- Parses first H1 heading as title
- First 150 chars of non-heading content as overview
- Uses file modification time for sorting

### 3. **Security**
- Path traversal prevention in `get_note`
- File size limits (1MB for content)
- Length limits (100 chars title, 255 chars overview)

### 4. **Error Handling**
- Structured JSON responses
- HTTP-style error codes (404, 403, 500)
- Detailed validation messages

### 5. **Flexibility**
- Optional search and date filters
- Auto-generated overview if not provided
- Case-insensitive search

## File Structure

```
notes-organizer/
├── notes/                    # Storage directory
│   ├── MCP.md
│   └── python-decorators.md
├── notes_organizer/
│   ├── __init__.py
│   └── main.py              # Server implementation
├── pyproject.toml           # Dependencies
└── README.md                # Documentation
```
