import asyncio
import random
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """Test client for notes-organizer MCP server."""
    # Define server parameters
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "main.py"],
        env=None
    )
    
    try:
        print("🔌 Connecting to notes-organizer MCP server...\n")
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                print("✓ Session established successfully!\n")
                
                # Step 1: List available tools
                print("📋 Listing available tools...")
                tools_list = await session.list_tools()
                
                print(f"✓ Found {len(tools_list.tools)} tools:\n")
                for tool in tools_list.tools:
                    print(f"  • {tool.name}")
                    print(f"    {tool.description}\n")
                
                # Step 2: Execute get_notes
                print("=" * 60)
                print("📚 Executing get_notes tool...")
                print("=" * 60)
                
                result = await session.call_tool("get_notes", arguments={})
                
                # Display the response from get_notes
                print("\n✓ get_notes tool executed successfully!\n")
                print("Response:")
                
                notes_data = None
                for content in result.content:
                    if hasattr(content, 'text'):
                        import json
                        notes_data = json.loads(content.text)
                        print(json.dumps(notes_data, indent=2))
                
                # Step 3: If notes exist, randomly select one and get its full content
                if notes_data and notes_data.get('success') and notes_data.get('notes'):
                    notes = notes_data['notes']
                    print(f"\n{'=' * 60}")
                    print(f"📝 Found {len(notes)} note(s). Selecting one randomly...")
                    print("=" * 60)
                    
                    # Randomly select a note
                    selected_note = random.choice(notes)
                    file_name = selected_note['file_name']
                    
                    print(f"\n🎯 Selected note: {file_name}")
                    print(f"   Title: {selected_note['title']}")
                    print(f"   Overview: {selected_note['overview']}\n")
                    
                    # Get full content of the selected note
                    print(f"📖 Fetching full content of '{file_name}'...")
                    note_result = await session.call_tool("get_note", arguments={"file_name": file_name})
                    
                    print("\n✓ get_note tool executed successfully!\n")
                    print("Full Note Content:")
                    print("=" * 60)
                    
                    for content in note_result.content:
                        if hasattr(content, 'text'):
                            import json
                            note_content = json.loads(content.text)
                            if note_content.get('success'):
                                print(note_content['content'])
                                print("=" * 60)
                                print(f"Size: {note_content['size_bytes']} bytes")
                                print(f"Modified: {note_content['modified_date']}")
                            else:
                                print(f"Error: {note_content.get('error')}")
                                print(f"Message: {note_content.get('message')}")
                else:
                    print("\n⚠️  No notes found or get_notes returned an empty list.")
                
                print("\n✓ All operations completed successfully!")
                
    except Exception as e:
        print(f"\n✗ Error occurred:")
        print(f"{type(e).__name__}: {str(e)}")
        import traceback
        print(traceback.format_exc())
    finally:
        print("\n🔌 Closing connection to MCP server...")
        print("👋 Client execution finished.")


if __name__ == "__main__":
    asyncio.run(main())
