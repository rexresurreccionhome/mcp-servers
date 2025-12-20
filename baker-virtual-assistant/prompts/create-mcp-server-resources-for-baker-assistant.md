# Prompt: Create a Resource for the Baker Virtual Assistant

## Overview

Implement a resource primitive type in the baker-virtual-assistant MCP Server. The resource will provide detailed recipe content for baking a Banana Loaf. This allows users to request recipe information through the MCP resource endpoint.

## Tasks

1. **Create a detailed Banana Loaf recipe**
   - Include precise measurements for all ingredients (using both imperial and metric units)
   - Provide complete step-by-step baking instructions
   - Include baking temperature and time
   - Add any helpful tips or notes for best results

2. **Implement a new resource endpoint in the MCP Server**
   - Resource URI: `recipe://banana-loaf`
   - Use the FastMCP `@mcp.resource()` decorator
   - The endpoint should expose the Banana Loaf recipe content

3. **Return the recipe content**
   - Format the recipe in a clear, readable structure
   - Include all ingredients with measurements
   - Include detailed preparation and baking instructions
   - Add any relevant notes or tips

## Technical Requirements

- Use the FastMCP library's resource decorator: `@mcp.resource()`
- Resource URI scheme: `recipe://`
- Resource name: `banana-loaf`
- Content type: Text/Markdown format
- Include a descriptive docstring for the resource function

## Acceptance Criteria

**Scenario 1: Resource Exposure**
- **Given:** The baker-virtual-assistant MCP Server is running
- **When:** The user opens the MCP Server Inspector
- **Then:** The resource `recipe://banana-loaf` is exposed and visible in the resources list

**Scenario 2: Recipe Retrieval**
- **Given:** The baker-virtual-assistant MCP Server is running
- **And:** The resource `recipe://banana-loaf` is exposed
- **When:** The user opens the MCP Server Inspector
- **And:** Submits a request to access the `recipe://banana-loaf` resource
- **Then:** The MCP Server returns the complete Banana Loaf recipe as a response

## Expected Recipe Structure

The recipe should include:
- Recipe title
- Yield/servings information
- Preparation time and baking time
- Ingredients list with precise measurements
- Step-by-step instructions
- Baking temperature and duration
- Optional: Tips for success, storage instructions, or variations

## Testing Steps

1. Start the MCP Server using `./mcp-run-dev.sh`
2. Open the MCP Server Inspector
3. Verify the resource `recipe://banana-loaf` appears in the resources list
4. Request the resource and verify the complete recipe is returned
5. Validate that the recipe content is properly formatted and readable
