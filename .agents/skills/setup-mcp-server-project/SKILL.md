---
name: setup-mcp-server-project
description: Set up a new MCP Server Python application. Use this skill to add the scaffoldings for a new MCP Server in this project. Utilize uv as package manager and FastMCP framework to build the server.
---
## Overview

Create a new MCP Server project so that the developer do not have to set up the scaffoldings from scratch. 

**IMPORTANT:** 

- Follow the Instructions carefully. Do not add morethan what has been explicitly mentioned.
- Follow the Project structure exactly as described in this skill.
- Only use the tools, libraries, and frameworks mentioned in the Prerequisites.


## Prerequisites

- [uv](https://docs.astral.sh/uv/) as package manager.
- [FastMCP](https://gofastmcp.com/getting-started/welcome) as Python framework for building the MCP Server.

## Project structure

```
project-folder/
  project_folder/
    main.py
  client.py <-- test mcp server integration by establishing a connection. Execute the operations from the mcp server
  mcp-install.sh
  mcp-run-dev.sh
  README.md
  run-client.sh
```

## Instructions

1. Start by asking the developer "What is the name of the new project?". Use the name to create the project-folder.
2. Use the hello-world MCP Server project template in this skill as a reference.
3. Create the new MCP Server project with `uv`.
4. Add `main.py` to initialize and run the MCP Server. 
5. Add utility bash scripts `mcp-install.sh`, `mcp-run-dev.sh` and `run-client.sh`
6. Run `run-client.sh` to verify that the scaffoloding is working.