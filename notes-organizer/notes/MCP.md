# About MCP

Learning about MCP and how it is being used by LLM to get context from external sources.

## MCP

**Model Context Protocol (MCP)**  - Is a standard (protocol) for AI that allows LLM to connect to external tools and data sources like databases, APIs, etc.

## MCP Host

Is the application or runtime (like chatbot or code editor) that uses the MCP to coordinate an AI agent's interactions with external tools and data.

## MCP Client 

Is acting as a consumer in the MCP. It is the component within the MCP Host that establishes a connection and handles the communication to an MCP Server.

## MCP Server

A server that implements the MCP, acting as an intermediary allowing AI agents to perform tasks, without needing to understand the underlying processes (APIs/tool/local data, etc.).

## AI Agent

Refers to an AI-powered assistant (tool) that can observe, make decision, and take actions to reach a goal. E.g. copilot, VA, chatbot, etc. The AI agent uses MCP to communicate with data, tools and other agents.

## Agentic AI
Is an Autonomous AI systems that can independently plan, decide, and execute actions to achieve goals with minimal human oversight.
