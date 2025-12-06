# Prompt: Create a Notes Organizer MCP Server with FastMCP

Using FastMCP help me create an MCP Server that has the functionality to read through my personal notes and return the results from each of the tools in a semi structured JSON format.

- add a tool called get_notes. This tool will read all md files inside the notes folder. The tool will accept parameters search, start_date and end_date. The tool must have the ability to search the notes by file name, content and modify date. The tool will return the File Name, Title and Overview.

- add a tool called get_note. This tool will read a specific md file inside the notes folder based on the given required parameter file_name. The tool will return the full content of the md file if it exists. Otherwise, return a 404 not found.
