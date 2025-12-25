# Create OpenAI-Integrated MCP Client for baker-virtual-assistant

## Objective

Create a lightweight OpenAI-integrated MCP Client that connects to the baker-virtual-assistant MCP Server, discovers available tools, prompts, and resources, and uses OpenAI's LLM to provide simple, cost-effective responses to user queries. This implements a minimal API usage pattern optimized for quota-limited scenarios.

## Requirements

### Implementation Tasks

1. **Create OpenAI-Integrated MCP Client** (`client_openai.py`)
   - Use the existing `client.py` as a structural reference
   - Implement async architecture for both MCP and OpenAI API calls
   - Handle concurrent connections to MCP server and OpenAI API

2. **Environment Configuration**
   - Create `.env` file in the `baker-virtual-assistant` directory
   - Store OpenAI API key: `OPENAI_API_KEY=your_api_key_here`
   - Add `.env` to the mcp-servers root `.gitignore` to prevent accidental commits
   - Include `.env.example` template for documentation

3. **Dependency Management**
   - Install `openai` Python library using uv: `uv pip install openai`
   - Install `python-dotenv` for environment variable management: `uv pip install python-dotenv`
   - Update `pyproject.toml` to include new dependencies

4. **OpenAI Integration Setup**
   - Initialize OpenAI client using API key from `.env`
   - Configure GPT model `gpt-3.5-turbo` (cost-effective choice)
   - Implement proper error handling for API failures and rate limits

5. **MCP Server Discovery & Tool Registration**
   - Connect to baker-virtual-assistant MCP server
   - Retrieve all available tools using `session.list_tools()`
   - Retrieve all available resources using `session.list_resources()`
   - Retrieve all available prompts using `session.list_prompts()`
   - Convert MCP tool schemas into OpenAI function calling format
   - Register MCP capabilities as available functions for the LLM

6. **Use MCP Server Prompt Template**
   - Retrieve the `baker_virtual_assistant` prompt using `session.get_prompt()`
   - Pass the user query as the `user_input` argument to get the prompt
   - Extract the system prompt content from the MCP server's prompt response
   - Use this MCP-provided prompt as the system message for OpenAI
   - This ensures the assistant behavior is consistent with the MCP server's definition

7. **Implement Agentic Loop with Cost Controls**
   - Send user query: "How to bake a dozen red velvet cupcakes?"
   - Limit iterations to 5 maximum to control API costs
   - Allow OpenAI to analyze available MCP tools and decide which to use
   - Execute OpenAI's tool calls against the MCP server
   - Return MCP results back to OpenAI for processing
   - Continue loop until OpenAI generates final response or max iterations reached
   - Display the complete conversation flow and final answer

8. **Verification & Output**
   - Display MCP server capabilities (tools, resources, prompts)
   - Log all MCP tool calls made by OpenAI (show which tools were selected)
   - Display intermediate results from MCP server
   - Show final processed response from OpenAI
   - Include statistics: iterations, tool calls, messages, tokens used

### Technical Specifications

- **MCP Library**: FastMCP or mcp Python SDK
- **AI Provider**: OpenAI GPT-3.5-turbo (cost-effective with function calling)
- **Max Iterations**: 5 iterations to control costs
- **Prompt Source**: MCP server's `baker_virtual_assistant` prompt template
- **Target MCP Server**: baker-virtual-assistant
- **Programming Pattern**: Async/await with agentic loop
- **Output Format**: Structured console output with clear sections
- **Error Handling**: Graceful handling of both MCP and OpenAI errors

## Architecture Overview

```
User Query
    ↓
OpenAI-Integrated MCP Client
    ↓
    ├──→ MCP Server Connection (Discovery)
    │    ├── List Tools (get_baking_tips, convert_temperature)
    │    ├── List Resources (recipe://banana-loaf, etc.)
    │    └── List Prompts (baker_virtual_assistant)
    │    └── Display capabilities to user
    │
    └──→ OpenAI API (Single Call)
         ├── Send simple query with brief system prompt
         ├── Receive direct response (no tool calling)
         └── Display answer to user
```

## Acceptance Criteria

### AC1: Environment Setup
**Given**: The baker-virtual-assistant project structure  
**When**: The developer sets up the OpenAI integration  
**Then**: 
- A `.env` file exists with `OPENAI_API_KEY` placeholder
- A `.env.example` file exists for documentation
- `.env` is listed in `.gitignore`
- Dependencies (`openai`, `python-dotenv`) are in `pyproject.toml`

### AC2: MCP Server Connection & Discovery
**Given**: The baker-virtual-assistant MCP Server is running  
**When**: The client initializes and connects to the MCP server  
**Then**: 
- Connection is established successfully
- All available tools are retrieved and logged
- All available resources are retrieved and logged
- All available prompts are retrieved and logged

### AC3: OpenAI Client Initialization
**Given**: A valid OpenAI API key is in the `.env` file  
**When**: The client starts  
**Then**: 
- OpenAI client initializes successfully
- API key is loaded from environment variables
- Connection to OpenAI API is verified

### AC4: Tool Schema Conversion
**Given**: MCP tools are retrieved from the server  
**When**: The client prepares tools for OpenAI  
**Then**: 
- MCP tool schemas are converted to OpenAI function calling format
- Each tool's name, description, and parameters are accurately mapped
- The tools array is compatible with OpenAI's API specification

### AC5: Simple Query Processing
**Given**: The MCP server is running and OpenAI client is initialized  
**When**: The user query "How to bake a dozen red velvet cupcakes?" is submitted  
**Then**: 
- Query is sent to OpenAI with simple system prompt
- Single API call is made (no tool calling)
- OpenAI generates a brief, direct response
- Response is limited to 300 tokens to minimize cost

### AC6: Complete Output Display
**Given**: The OpenAI call has completed  
**When**: The final response is generated  
**Then**: 
- MCP server capabilities are displayed
- Final OpenAI response is displayed
- Statistics are shown (tokens used)
- Output is clear and concise

## Expected Deliverables

1. **`client_openai.py`** - OpenAI-integrated MCP client in `baker-virtual-assistant/` directory
2. **`.env.example`** - Template for environment variables
3. **`.gitignore` update** - Ensure `.env` is excluded from version control
4. **`pyproject.toml` update** - Include `openai` and `python-dotenv` dependencies
5. **`run-client-openai.sh`** - Shell script to execute the OpenAI client
6. **README update** - Document the new OpenAI client usage (optional)

## Example Output Structure

```
================================================================================
        OpenAI-Integrated Baker Virtual Assistant
================================================================================

🔌 Connecting to baker-virtual-assistant MCP server...

✓ MCP Server connection established!

================================================================================
[1] Discovering MCP Server Capabilities...
================================================================================

📦 Found 2 tools:
  • get_baking_tips: Get helpful baking tips and advice
  • convert_temperature: Convert Fahrenheit to Celsius for baking

📚 Found 1 resources:
  • recipe://banana-loaf: Complete recipe for baking a delicious Banana Loaf

💬 Found 1 prompts:
  • baker_virtual_assistant: A master baker virtual assistant

================================================================================
[2] Registering MCP Tools with OpenAI...
================================================================================

✓ Registered 2 tools with OpenAI LLM

================================================================================
[3] User Query
================================================================================
❓ How to bake a dozen red velvet cupcakes?

================================================================================
[4] Starting Agentic Loop...
================================================================================

🔄 Requesting response from OpenAI...
────────────────────────────────────────────────────────────────────────────

================================================================================
[5] Final Response
================================================================================

To bake a dozen red velvet cupcakes:

1. Preheat oven to 350°F (175°C)
2. Mix dry ingredients: 1½ cups flour, 1 cup sugar, 1 tbsp cocoa powder, 
   ½ tsp baking soda, ½ tsp salt
3. Mix wet ingredients: 1 cup buttermilk, ½ cup oil, 2 eggs, 2 tbsp red food 
   coloring, 1 tsp vanilla, 1 tsp vinegar
4. Combine wet and dry ingredients until just mixed
5. Fill cupcake liners ⅔ full
6. Bake 18-20 minutes until toothpick comes out clean
7. Cool and frost with cream cheese frosting

================================================================================
[6] Statistics
================================================================================

🛠️  Total tool calls: 0
🔢 Total tokens used: 245
   - Prompt tokens: 65
   - Completion tokens: 180

================================================================================
                    ✅ Session Completed Successfully
================================================================================
```

## Implementation Notes

### Simple Query Processing Pattern

The client makes a single, direct API call without tool integration:

```python
# Simple messages setup
messages = [
    {
        "role": "system",
        "content": "You are a helpful baking assistant. Answer briefly."
    },
    {
        "role": "user",
        "content": user_query
    }
]

# Single API call - no tools, no iterations
response = openai_client.chat.completions.create(
    model="gpt-3.5-turbo",      # Cost-effective model
    messages=messages,
    max_tokens=300,              # Limit response length
    temperature=0.7
)

# Extract and display the response
assistant_message = response.choices[0].message
print(assistant_message.content)
```

### Error Handling Considerations

- **MCP Server Unavailable**: Provide clear error message and exit gracefully
- **OpenAI API Errors**: Handle rate limits, invalid API key, network issues, quota exceeded errors
- **Missing API Key**: Validate `.env` file exists and contains `OPENAI_API_KEY`

## Testing Checklist

- [ ] `.env` file created with valid OpenAI API key
- [ ] `.env` is in root `.gitignore`
- [ ] Dependencies installed successfully (`openai`, `python-dotenv`)
- [ ] MCP server starts and client connects
- [ ] OpenAI client initializes with API key
- [ ] All MCP tools are discovered and displayed
- [ ] User query is processed by OpenAI
- [ ] Single API call returns a response
- [ ] Response is limited to 300 tokens
- [ ] Final response is displayed clearly
- [ ] Token usage statistics are shown

## Future Enhancements (Optional)

- Upgrade to full agentic loop with tool calling when quota allows
- Add support for streaming responses from OpenAI
- Implement conversation history for multi-turn interactions
- Add retry logic with exponential backoff for API calls
- Create a simple CLI for interactive queries
- Add support for switching between different OpenAI models (gpt-4o, etc.)
- Implement cost tracking for OpenAI API usage
- Add caching for frequently used responses
