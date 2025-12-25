import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Test client for baker-virtual-assistant MCP server."""
    # Define server parameters
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "baker_virtual_assistant/main.py"],
        env=None
    )
    
    try:
        print("=" * 80)
        print("Baker Virtual Assistant MCP Client Test".center(80))
        print("=" * 80)
        print()
        
        print("🔌 Connecting to baker-virtual-assistant MCP server...\n")
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                print("✓ Connection established successfully!\n")
                
                # [1] List available tools
                print("=" * 80)
                print("[1] Listing Available Tools...")
                print("=" * 80)
                
                tools_list = await session.list_tools()
                
                if tools_list.tools:
                    for tool in tools_list.tools:
                        print(f"  • {tool.name}: {tool.description}")
                else:
                    print("  No tools found.")
                print()
                
                # [2] List available prompts
                print("=" * 80)
                print("[2] Listing Available Prompts...")
                print("=" * 80)
                
                prompts_list = await session.list_prompts()
                
                if prompts_list.prompts:
                    for prompt in prompts_list.prompts:
                        print(f"  • {prompt.name}: {prompt.description}")
                else:
                    print("  No prompts found.")
                print()
                
                # [3] List available resources
                print("=" * 80)
                print("[3] Listing Available Resources...")
                print("=" * 80)
                
                resources_list = await session.list_resources()
                
                if resources_list.resources:
                    for resource in resources_list.resources:
                        print(f"  • {resource.uri}: {resource.name}")
                else:
                    print("  No resources found.")
                print()
                
                # [4] Test Tool: get_baking_tips
                print("=" * 80)
                print("[4] Testing Tool: get_baking_tips")
                print("=" * 80)
                
                tips_result = await session.call_tool("get_baking_tips", arguments={})
                
                print("\nResponse:")
                for content in tips_result.content:
                    if hasattr(content, 'text'):
                        print(content.text)
                print()
                
                # [5] Test Tool: convert_temperature
                print("=" * 80)
                print("[5] Testing Tool: convert_temperature (350°F)")
                print("=" * 80)
                
                temp_result = await session.call_tool(
                    "convert_temperature", 
                    arguments={"fahrenheit": 350}
                )
                
                print("\nResponse:")
                for content in temp_result.content:
                    if hasattr(content, 'text'):
                        result_data = json.loads(content.text)
                        print(f"  {result_data['fahrenheit']}°F = {result_data['celsius']}°C")
                print()
                
                # [6] Test Resource: recipe://banana-loaf
                print("=" * 80)
                print("[6] Testing Resource: recipe://banana-loaf")
                print("=" * 80)
                
                recipe_result = await session.read_resource("recipe://banana-loaf")
                
                print("\nResponse:")
                for content in recipe_result.contents:
                    if hasattr(content, 'text'):
                        # Print first 500 characters of the recipe
                        recipe_text = content.text
                        if len(recipe_text) > 500:
                            print(recipe_text[:500] + "...")
                            print(f"\n  [Recipe truncated - Total length: {len(recipe_text)} characters]")
                        else:
                            print(recipe_text)
                print()
                
                # [7] Test Prompt: baker_virtual_assistant
                print("=" * 80)
                print('[7] Testing Prompt: baker_virtual_assistant ("how to bake chocolate chip cookies")')
                print("=" * 80)
                
                prompt_result = await session.get_prompt(
                    "baker_virtual_assistant",
                    arguments={"user_input": "how to bake chocolate chip cookies"}
                )
                
                print("\nResponse:")
                if prompt_result.messages:
                    for message in prompt_result.messages:
                        if hasattr(message.content, 'text'):
                            prompt_text = message.content.text
                            # Print first 500 characters of the prompt
                            if len(prompt_text) > 500:
                                print(prompt_text[:500] + "...")
                                print(f"\n  [Prompt truncated - Total length: {len(prompt_text)} characters]")
                            else:
                                print(prompt_text)
                print()
                
                # Test completed
                print("=" * 80)
                print("Test Completed Successfully".center(80))
                print("=" * 80)
                
    except Exception as e:
        print(f"\n❌ Error occurred: {type(e).__name__}")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
