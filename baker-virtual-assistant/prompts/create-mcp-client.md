# Create MCP Client for baker-virtual-assistant

## Objective

Create an MCP Client that connects to the baker-virtual-assistant MCP Server to retrieve available tools, prompts, and resources. The client will execute actions to test the MCP Server functionality and print outputs for verification.

## Requirements

### Implementation Tasks

1. **Create an MCP Client** using the FastMCP library
2. **Establish Connection** to the baker-virtual-assistant MCP Server
3. **List Available Tools** from the MCP Server
4. **List Available Prompts** from the MCP Server
5. **List Available Resources** from the MCP Server
6. **Execute Commands** to utilize the tools, prompts, and resources
7. **Display Output** from the MCP Server in a readable format
8. **Close Connection** gracefully after execution completes

### Technical Specifications

- **Library**: FastMCP
- **Target Server**: baker-virtual-assistant
- **Output Format**: Clearly formatted console output with section headers
- **Error Handling**: Handle connection failures and server errors gracefully

## Acceptance Criteria

### AC1: List Available Tools
**Given**: The baker-virtual-assistant MCP Server is running  
**When**: The client requests to list all available tools  
**Then**: The MCP Server available tools are displayed

### AC2: List Available Prompts
**Given**: The baker-virtual-assistant MCP Server is running  
**When**: The client requests to list all available prompts  
**Then**: The MCP Server available prompts are displayed

### AC3: List Available Resources
**Given**: The baker-virtual-assistant MCP Server is running  
**When**: The client requests to list all available resources  
**Then**: The MCP Server available resources are displayed

### AC4: Retrieve Banana Loaf Recipe
**Given**: The baker-virtual-assistant MCP Server is running  
**When**: The client requests the banana loaf recipe (resource: `recipe://banana-loaf`)  
**Then**: The MCP Server returns the complete recipe for baking a banana loaf

### AC5: Get Baking Tips
**Given**: The baker-virtual-assistant MCP Server is running  
**When**: The client requests baking tips (tool: `get_baking_tips`)  
**Then**: The MCP Server returns helpful tips for baking

### AC6: Convert Temperature
**Given**: The baker-virtual-assistant MCP Server is running  
**When**: The client requests to convert 350°F to Celsius (tool: `convert_temperature`)  
**Then**: The MCP Server returns the converted temperature in Celsius (175°C)

### AC7: Use Baker Assistant Prompt
**Given**: The baker-virtual-assistant MCP Server is running  
**When**: The client requests to generate a prompt for "how to bake chocolate chip cookies"  
**Then**: The MCP Server returns the formatted prompt for the baker virtual assistant with the user's question

## Expected Deliverables

1. A Python client script (`client.py`) in the `baker-virtual-assistant` directory
2. Executable shell script (`run-client.sh`) to simplify running the client
3. Clear console output demonstrating all functionality working correctly

## Example Output Structure

The client should produce output similar to:

```
========================================
Baker Virtual Assistant MCP Client Test
========================================

[1] Listing Available Tools...
- get_baking_tips: Get helpful baking tips and advice
- convert_temperature: Convert Fahrenheit to Celsius for baking

[2] Listing Available Prompts...
- baker_virtual_assistant: A master baker virtual assistant that provides expert baking advice and instructions

[3] Listing Available Resources...
- recipe://banana-loaf: Complete recipe for baking a delicious Banana Loaf

[4] Testing Tool: get_baking_tips
Response:
<output>

[5] Testing Tool: convert_temperature (350°F)
Response:
<output>

[6] Testing Resource: recipe://banana-loaf
Response:
<output>

[7] Testing Prompt: baker_virtual_assistant ("how to bake chocolate chip cookies")
Response:
<output>

========================================
Test Completed Successfully
========================================
```

## Notes

- Ensure the MCP Server is running before executing the client
- The client should handle connection timeouts gracefully
- All outputs should be clearly labeled for easy verification
- Consider adding color-coded output for better readability (optional)
