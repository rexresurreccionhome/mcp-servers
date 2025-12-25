import asyncio
import json
import os
from typing import Any
from dotenv import load_dotenv
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def convert_mcp_tool_to_openai(mcp_tool: Any) -> dict:
    """Convert MCP tool schema to OpenAI function calling format."""
    function_def = {
        "type": "function",
        "function": {
            "name": mcp_tool.name,
            "description": mcp_tool.description or "",
        }
    }
    
    # Add parameters if they exist
    if hasattr(mcp_tool, 'inputSchema') and mcp_tool.inputSchema:
        function_def["function"]["parameters"] = mcp_tool.inputSchema
    else:
        # Default empty parameters
        function_def["function"]["parameters"] = {
            "type": "object",
            "properties": {},
            "required": []
        }
    
    return function_def


async def main():
    """OpenAI-integrated MCP client for baker-virtual-assistant."""
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in .env file")
        print("Please create a .env file with your OpenAI API key.")
        print("See .env.example for template.")
        return
    
    # Initialize OpenAI client
    openai_client = OpenAI(api_key=api_key)
    
    # Define MCP server parameters
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "baker_virtual_assistant/main.py"],
        env=None
    )
    
    try:
        print("=" * 80)
        print("OpenAI-Integrated Baker Virtual Assistant".center(80))
        print("=" * 80)
        print()
        
        print("🔌 Connecting to baker-virtual-assistant MCP server...\n")
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the MCP connection
                await session.initialize()
                print("✓ MCP Server connection established!\n")
                
                # [1] Discover MCP Server Capabilities
                print("=" * 80)
                print("[1] Discovering MCP Server Capabilities...")
                print("=" * 80)
                print()
                
                # List available tools
                tools_list = await session.list_tools()
                print(f"📦 Found {len(tools_list.tools)} tools:")
                for tool in tools_list.tools:
                    print(f"  • {tool.name}: {tool.description}")
                print()
                
                # List available resources
                resources_list = await session.list_resources()
                print(f"📚 Found {len(resources_list.resources)} resources:")
                for resource in resources_list.resources:
                    print(f"  • {resource.uri}: {resource.name}")
                print()
                
                # List available prompts
                prompts_list = await session.list_prompts()
                print(f"💬 Found {len(prompts_list.prompts)} prompts:")
                for prompt in prompts_list.prompts:
                    print(f"  • {prompt.name}: {prompt.description}")
                print()
                
                # [2] Convert MCP tools to OpenAI function format
                print("=" * 80)
                print("[2] Registering MCP Tools with OpenAI...")
                print("=" * 80)
                print()
                
                openai_tools = [convert_mcp_tool_to_openai(tool) for tool in tools_list.tools]
                print(f"✓ Registered {len(openai_tools)} tools with OpenAI LLM")
                print()
                
                # [3] Get MCP Server Prompt Template
                print("=" * 80)
                print("[3] Getting MCP Server Prompt Template...")
                print("=" * 80)
                print()
                
                user_query = "How to bake a dozen red velvet cupcakes?"
                
                # Get the prompt template from MCP server
                prompt_result = await session.get_prompt(
                    "baker_virtual_assistant",
                    arguments={"user_input": user_query}
                )
                
                # Extract the prompt content
                system_prompt = ""
                if prompt_result.messages:
                    for message in prompt_result.messages:
                        if hasattr(message.content, 'text'):
                            system_prompt = message.content.text
                            break
                
                print(f"✓ Retrieved prompt template from MCP server")
                print(f"  Preview: {system_prompt[:150]}...")
                print()
                
                # [4] User Query
                print("=" * 80)
                print("[4] User Query")
                print("=" * 80)
                print(f"❓ {user_query}")
                print()
                
                # [5] Agentic Loop with OpenAI
                print("=" * 80)
                print("[5] Starting Agentic Loop...")
                print("=" * 80)
                print()
                
                # Initialize conversation with MCP server's prompt template
                messages = [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_query
                    }
                ]
                
                iteration = 0
                max_iterations = 5  # Limit iterations to control costs
                total_tool_calls = 0
                
                while iteration < max_iterations:
                    iteration += 1
                    print(f"🔄 Iteration {iteration}")
                    print("-" * 80)
                    
                    # Call OpenAI with available tools
                    response = openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=messages,
                        tools=openai_tools if openai_tools else None,
                        tool_choice="auto"
                    )
                    
                    assistant_message = response.choices[0].message
                    messages.append(assistant_message)
                    
                    # Check if OpenAI wants to call tools
                    if assistant_message.tool_calls:
                        print(f"🛠️  OpenAI requested {len(assistant_message.tool_calls)} tool call(s):")
                        
                        for tool_call in assistant_message.tool_calls:
                            tool_name = tool_call.function.name
                            tool_args = json.loads(tool_call.function.arguments)
                            total_tool_calls += 1
                            
                            print(f"  • Calling: {tool_name}")
                            print(f"    Arguments: {tool_args}")
                            
                            # Execute the tool on MCP server
                            try:
                                result = await session.call_tool(tool_name, arguments=tool_args)
                                
                                # Extract text content from result
                                tool_result = ""
                                for content in result.content:
                                    if hasattr(content, 'text'):
                                        tool_result += content.text
                                
                                print(f"    Result: {tool_result[:200]}{'...' if len(tool_result) > 200 else ''}")
                                
                                # Add tool result to messages
                                messages.append({
                                    "role": "tool",
                                    "tool_call_id": tool_call.id,
                                    "content": tool_result
                                })
                                
                            except Exception as e:
                                error_msg = f"Error calling tool {tool_name}: {str(e)}"
                                print(f"    ❌ {error_msg}")
                                messages.append({
                                    "role": "tool",
                                    "tool_call_id": tool_call.id,
                                    "content": error_msg
                                })
                        
                        print()
                    
                    # Check if we have a final response
                    elif assistant_message.content:
                        print("✅ OpenAI generated final response")
                        print()
                        break
                    
                    else:
                        print("⚠️  No tool calls or content in response")
                        break
                print()
                
                # [6] Display Final Response
                print("=" * 80)
                print("[6] Final Response")
                print("=" * 80)
                print()
                
                final_message = messages[-1]
                if hasattr(final_message, 'content') and final_message.content:
                    print(final_message.content)
                elif isinstance(final_message, dict) and 'content' in final_message:
                    print(final_message['content'])
                else:
                    print("No final response generated")
                
                print()
                
                # [7] Statistics
                print("=" * 80)
                print("[7] Statistics")
                print("=" * 80)
                print()
                print(f"📊 Total iterations: {iteration}")
                print(f"🛠️  Total tool calls: {total_tool_calls}")
                print(f"💬 Total messages: {len(messages)}")
                print(f"🔢 Total tokens used: {response.usage.total_tokens}")
                print(f"   - Prompt tokens: {response.usage.prompt_tokens}")
                print(f"   - Completion tokens: {response.usage.completion_tokens}")
                print()
                print("=" * 80)
                print("✅ Session Completed Successfully".center(80))
                print("=" * 80)
                
    except Exception as e:
        print(f"\n❌ Error occurred: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
