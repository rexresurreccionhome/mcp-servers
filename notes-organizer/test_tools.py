"""Test script to verify the MCP tools work correctly."""
import json
from main import get_notes, get_note

print("=" * 60)
print("Testing Notes Organizer MCP Server Tools")
print("=" * 60)

# Test 1: Get all notes
print("\n1. Testing get_notes() - Get all notes:")
result = get_notes()
print(json.dumps(result, indent=2))

# Test 2: Search for notes containing "MCP"
print("\n2. Testing get_notes(search='MCP'):")
result = get_notes(search="MCP")
print(json.dumps(result, indent=2))

# Test 3: Search for notes containing "protocol"
print("\n3. Testing get_notes(search='protocol'):")
result = get_notes(search="protocol")
print(json.dumps(result, indent=2))

# Test 4: Get a specific note
print("\n4. Testing get_note(file_name='MCP.md'):")
result = get_note(file_name="MCP.md")
print(json.dumps(result, indent=2))

# Test 5: Try to get a non-existent note (should return 404)
print("\n5. Testing get_note(file_name='nonexistent.md') - Should return 404:")
result = get_note(file_name="nonexistent.md")
print(json.dumps(result, indent=2))

# Test 6: Get note without .md extension (should auto-append)
print("\n6. Testing get_note(file_name='MCP') - Without extension:")
result = get_note(file_name="MCP")
print(json.dumps(result, indent=2))

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
