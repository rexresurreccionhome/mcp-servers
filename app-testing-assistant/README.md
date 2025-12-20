# App Testing Assistant MCP Server

An MCP (Model Context Protocol) server that helps QA testers and new developers learn how to write integration tests for your application's APIs. This server provides interactive documentation, test examples, and code generation tools to accelerate the learning process.

## Overview

The App Testing Assistant transforms your LLM into a specialized QA testing tutor that:
- Provides complete API documentation and schemas
- Shows real-world test examples
- Generates test payloads on demand
- Suggests proper assertions for different scenarios
- Teaches testing best practices interactively

## Use Cases

- **Onboarding New QA Engineers**: Help them understand your API structure and testing patterns
- **Teaching Integration Testing**: Provide hands-on examples and guidance
- **Standardizing Test Practices**: Ensure consistent testing approaches across the team
- **Rapid Test Development**: Generate boilerplate test code quickly
- **API Documentation**: Living, interactive API reference

## Features

### 📚 Resources (Context for LLMs)

#### 1. API Schema Documentation
**URI**: `api://schema/user-service`

Complete API documentation including:
- All available endpoints
- Request/response formats
- Validation rules
- Error codes and responses
- Field requirements and types

#### 2. Test Examples
**URI**: `api://examples/user-service-tests`

Real-world integration test examples:
- Happy path scenarios
- Validation error tests
- Duplicate data handling
- Update operations
- Proper test structure (AAA pattern)

#### 3. Testing Guidelines
**URI**: `testing://guidelines/integration-tests`

Best practices documentation:
- Test structure patterns
- What to test and assert
- Test data management
- Common mistakes to avoid
- Assertion checklists

### 🛠️ Tools (Interactive Helpers)

#### 1. `generate_test_payload(endpoint, scenario)`

Generates sample API payloads for different test scenarios.

**Parameters:**
- `endpoint` (string): The API endpoint (e.g., "POST /users")
- `scenario` (string): The test scenario (e.g., "valid", "missing_email", "invalid_format")

**Returns:**
```json
{
  "endpoint": "POST /users",
  "scenario": "valid",
  "payload": {
    "email": "testuser@example.com",
    "username": "testuser123",
    "firstName": "Test",
    "lastName": "User",
    "role": "user"
  }
}
```

**Example Usage:**
- "Generate a payload for creating a user with invalid email"
- "What payload should I use for testing duplicate users?"

#### 2. `validate_test_assertions(endpoint, response_status)`

Provides recommended assertions for testing specific endpoint responses.

**Parameters:**
- `endpoint` (string): The API endpoint being tested
- `response_status` (int): The HTTP status code (200, 201, 400, 404, etc.)

**Returns:**
```json
{
  "endpoint": "POST /users",
  "status_code": 201,
  "assertions": {
    "status_code": "assert response.status_code == 201",
    "required_fields": [
      "assert 'id' in data",
      "assert 'email' in data"
    ],
    "field_values": [
      "assert data['email'] == payload['email']"
    ]
  }
}
```

**Example Usage:**
- "What should I assert for a successful user creation?"
- "What assertions are needed for a 404 response?"

### 💬 Prompts

#### `qa_testing_assistant()`

A specialized prompt that configures the LLM to act as a QA Testing Assistant with expertise in:
- Writing integration tests using Python and pytest
- API testing best practices
- Understanding API schemas and payloads
- Debugging test failures
- Test data management

## Installation

1. **Install dependencies:**
```bash
./mcp-install.sh
```

Or manually:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

2. **Configure Claude Desktop** (or your MCP client):

Edit your Claude Desktop config file:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:
```json
{
  "mcpServers": {
    "app-testing-assistant": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/app-testing-assistant",
        "run",
        "app-testing-assistant"
      ]
    }
  }
}
```

## Usage Examples

### Example 1: Learning About an API Endpoint

**User:** "What's the API for creating a user?"

**LLM Response:** *(reads `api://schema/user-service` resource)*
```
The POST /users endpoint creates a new user account.

Request Payload:
{
  "email": "string (required, valid email format)",
  "username": "string (required, 3-20 characters)",
  "firstName": "string (required)",
  "lastName": "string (required)",
  "role": "string (optional: 'user', 'admin', 'qa')"
}

Success Response (201): Returns the created user object with id and timestamps.
```

### Example 2: Writing a Test

**User:** "Write an integration test for creating a user with a duplicate email"

**LLM Response:** *(uses resources + tools)*
```python
import pytest
import requests

def test_create_user_duplicate_email():
    # Arrange - Create initial user
    payload = {
        "email": "duplicate@example.com",
        "username": "user1",
        "firstName": "First",
        "lastName": "User"
    }
    requests.post("https://api.yourapp.com/v1/users", json=payload)
    
    # Arrange - Try to create duplicate
    duplicate_payload = {
        "email": "duplicate@example.com",  # Same email
        "username": "user2",  # Different username
        "firstName": "Second",
        "lastName": "User"
    }
    
    # Act
    response = requests.post(
        "https://api.yourapp.com/v1/users",
        json=duplicate_payload
    )
    
    # Assert
    assert response.status_code == 409
    data = response.json()
    assert "error" in data
    assert "already exists" in data["error"].lower()
```

### Example 3: Getting Test Assertions

**User:** "What should I assert for a 201 response when creating a user?"

**LLM Response:** *(calls `validate_test_assertions` tool)*
```python
# Status code
assert response.status_code == 201

# Required fields are present
assert 'id' in data
assert 'email' in data
assert 'username' in data
assert 'createdAt' in data
assert 'updatedAt' in data

# Field values match expectations
assert data['email'] == payload['email']
assert data['username'] == payload['username']
assert data['isActive'] == True

# Data types are correct
assert isinstance(data['id'], str)
assert isinstance(data['isActive'], bool)
```

### Example 4: Learning Best Practices

**User:** "What are the best practices for integration testing?"

**LLM Response:** *(reads `testing://guidelines/integration-tests` resource)*
```
Integration Testing Best Practices:

1. Test Structure (AAA Pattern):
   - Arrange: Set up test data
   - Act: Execute the API call
   - Assert: Verify the response

2. What to Test:
   ✓ Happy path scenarios
   ✓ Validation errors
   ✓ Business logic errors
   ✓ Edge cases

3. Assertions Checklist:
   ✓ HTTP status code
   ✓ Response body structure
   ✓ Required fields present
   ✓ Data types correct
   ✓ Values match expectations

4. Common Mistakes to Avoid:
   ✗ Hard-coding production IDs
   ✗ Not cleaning up test data
   ✗ Testing multiple things in one test
   ✗ Not testing error scenarios
```

## Development

### Running the Server

**Development mode:**
```bash
./mcp-run-dev.sh
```

Or manually:
```bash
uv run mcp dev main.py
```

This will:
- Start the MCP server
- Open the MCP Inspector UI
- Show available resources, tools, and prompts
- Allow you to test functionality interactively

### Testing Resources and Tools

Once the MCP Inspector is running:

1. **Test Resources:**
   - Navigate to the Resources tab
   - Click on `api://schema/user-service`
   - Verify the API documentation displays correctly

2. **Test Tools:**
   - Navigate to the Tools tab
   - Call `generate_test_payload` with parameters:
     - endpoint: "POST /users"
     - scenario: "valid"
   - Verify it returns a proper payload

3. **Test Prompts:**
   - Navigate to the Prompts tab
   - View the `qa_testing_assistant` prompt
   - Verify it contains the proper instructions

## Customization

### Adding New API Endpoints

1. **Update the schema resource:**
   ```python
   @mcp.resource("api://schema/user-service")
   def user_service_api_schema() -> str:
       # Add your endpoint documentation here
   ```

2. **Add test examples:**
   ```python
   @mcp.resource("api://examples/user-service-tests")
   def user_service_test_examples() -> str:
       # Add example tests for the new endpoint
   ```

3. **Update the payload generator:**
   ```python
   @mcp.tool()
   def generate_test_payload(endpoint: str, scenario: str) -> dict:
       payloads = {
           "POST /your-new-endpoint": {
               "valid": { ... },
               "invalid": { ... }
           }
       }
   ```

4. **Update the assertions helper:**
   ```python
   @mcp.tool()
   def validate_test_assertions(endpoint: str, response_status: int) -> dict:
       assertions = {
           "POST /your-new-endpoint": {
               201: { ... },
               400: { ... }
           }
       }
   ```

### Adding New Services

To document multiple services (e.g., User Service, Order Service, Product Service):

1. Create separate resources for each service:
   ```python
   @mcp.resource("api://schema/order-service")
   def order_service_api_schema() -> str:
       # Order service documentation
   
   @mcp.resource("api://schema/product-service")
   def product_service_api_schema() -> str:
       # Product service documentation
   ```

2. Create corresponding test examples for each service

3. Update tools to handle multiple services using a `service` parameter

## Architecture

```
┌─────────────────────────────────────────────┐
│           LLM (Claude, GPT, etc.)          │
│                                             │
│  "Write a test for creating a user with    │
│   an invalid email address"                │
└──────────────────┬──────────────────────────┘
                   │ MCP Protocol
                   ↓
┌─────────────────────────────────────────────┐
│     App Testing Assistant MCP Server        │
│                                             │
│  Resources:                                 │
│  • API Schema Documentation                 │
│  • Test Examples                           │
│  • Testing Guidelines                      │
│                                             │
│  Tools:                                     │
│  • generate_test_payload()                 │
│  • validate_test_assertions()              │
│                                             │
│  Prompts:                                   │
│  • qa_testing_assistant()                  │
└─────────────────────────────────────────────┘
```

## Benefits

1. **Faster Onboarding**: New team members learn API structure quickly
2. **Consistent Testing**: Everyone follows the same patterns and best practices
3. **Living Documentation**: API docs that stay up-to-date with code
4. **Reduced Errors**: Proper assertions and test structure from the start
5. **Knowledge Sharing**: Captures team's testing expertise in one place
6. **Interactive Learning**: Learn by doing, not just reading docs

## Future Enhancements

Potential additions:
- Generate complete test files with fixtures
- Integration with your actual API (make real test calls)
- Test coverage analysis
- Generate test data factories
- Mock data generation
- API contract validation
- Performance testing examples
- Security testing patterns

## License

MIT

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
