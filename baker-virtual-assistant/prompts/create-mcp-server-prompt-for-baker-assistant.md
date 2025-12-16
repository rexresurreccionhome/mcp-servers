# Prompt: Create a prompt for a baker assistant

## Tasks

1. Using the FastMCP library, I want to expose a prompt template for the baker-virtual-assistant called `baker_virtual_assistant`.
2. Add a new function that will return the predefined prompt template
3. The function will accept a required parameter `user_input`
4. Set the persona in the prompt template. 
    - The virtual assistant will only focus on answering questions related to Baking.
    - The virtual assistant is a master baker.
    - The virtual assistant will refuse to answer questions that are not related to baking with a message "Sorry I do not understand the question"
    - The virtual assistant will give a step by step instructions that is user friendly.
    - At the end of every response, create a summary and return the sources for user reference.

## Acceptance Criteria
Given: The baker-virtual-assistant MCP Server is running
When: The user opens the MCP Server Inspector
Then: The prompt `baker_virtual_assistant` is exposed

Given: The baker-virtual-assistant MCP Server is running
And: The prompt `baker_virtual_assistant` is exposed
When: The user opens the MCP Server Inspector
And: Submit a question related to baking to the `baker_virtual_assistant` prompt
Then: The MCP Server answers the questions with a user friendly response.

Given: The baker-virtual-assistant MCP Server is running
And: The prompt `baker_virtual_assistant` is exposed
When: The user opens the MCP Server Inspector
And: Submit a question that is NOT related to baking to the `baker_virtual_assistant` prompt
Then: The MCP Server decline to answer the questions with a message "Sorry I do not understand the question".

