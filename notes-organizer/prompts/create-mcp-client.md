Help me create a client that I can run as a python script to test the functionality of my mcp server.

- add a new client python module. Using mcp library, StdioServerParameters and asyncio, connect to my notes-organizer mcp server.

- the module must establish a client session

- when a session has been established, the first action that I want to do is list all the tools available from the mcp server

- after successfully listing all tools. Execute get_notes

- Display the response from get_notes tool

- If the get_notes returns a non empty list, randomly select a note and get the full content of the note using get_note

- finally close the connection to the mcp server and exit the client execution