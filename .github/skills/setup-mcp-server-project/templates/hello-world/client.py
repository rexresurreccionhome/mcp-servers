import asyncio
import traceback
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


async def main():
    # Define server parameters
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "hello_world/main.py"],
        env=None
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                
                # List available tools
                print("Fetching list of tools...")
                tools_list = await session.list_tools()
                
                print(f"\n✓ Successfully retrieved {len(tools_list.tools)} tools:")
                for tool in tools_list.tools:
                    print(f"  - {tool.name}: {tool.description}")
                
                # Call the simple_hello_world_poem tool
                print("\nExecuting simple_hello_world_poem tool...")
                result = await session.call_tool("simple_hello_world_poem", arguments={})
                
                print("\n✓ Tool execution successful!")
                print("\nResult:")
                for content in result.content:
                    if hasattr(content, 'text'):
                        print(content.text)
                    
    except Exception as e:
        print(f"\n✗ Error occurred:")
        print(traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())

