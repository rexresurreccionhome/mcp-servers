from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP("app-testing-assistant")


# RESOURCES - Provide context about your application
@mcp.resource("api://schema/user-service")
def user_service_api_schema() -> str:
    """Complete API schema and documentation for the User Service"""
    return """# User Service API Documentation

## Base URL
`https://api.yourapp.com/v1`

## Endpoints

### POST /users
Create a new user account

**Request Payload:**
```json
{
  "email": "string (required, valid email format)",
  "username": "string (required, 3-20 characters, alphanumeric)",
  "firstName": "string (required)",
  "lastName": "string (required)",
  "role": "string (optional, enum: 'user', 'admin', 'qa')",
  "isActive": "boolean (optional, default: true)"
}
```

**Success Response (201):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "username": "johndoe",
  "firstName": "John",
  "lastName": "Doe",
  "role": "user",
  "isActive": true,
  "createdAt": "2025-12-20T10:30:00Z",
  "updatedAt": "2025-12-20T10:30:00Z"
}
```

**Error Responses:**
- 400: Invalid payload (missing required fields, invalid email format)
- 409: User already exists (duplicate email or username)

**Validation Rules:**
- Email must be unique across all users
- Username must be unique and contain only alphanumeric characters
- Password must be at least 8 characters (if authentication enabled)

---

### GET /users/{userId}
Retrieve user details by ID

**Path Parameters:**
- `userId` (uuid, required)

**Success Response (200):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "username": "johndoe",
  "firstName": "John",
  "lastName": "Doe",
  "role": "user",
  "isActive": true,
  "createdAt": "2025-12-20T10:30:00Z",
  "updatedAt": "2025-12-20T10:30:00Z"
}
```

**Error Responses:**
- 404: User not found
- 403: Insufficient permissions

---

### PATCH /users/{userId}
Update user information

**Request Payload (all fields optional):**
```json
{
  "firstName": "string",
  "lastName": "string",
  "role": "string (enum: 'user', 'admin', 'qa')",
  "isActive": "boolean"
}
```

**Success Response (200):**
Returns updated user object

**Error Responses:**
- 400: Invalid payload
- 404: User not found
- 409: Conflict (e.g., trying to deactivate last admin)

---

### DELETE /users/{userId}
Soft delete a user (sets isActive to false)

**Success Response (204):**
No content

**Error Responses:**
- 404: User not found
- 409: Cannot delete last admin user
"""


@mcp.resource("api://examples/user-service-tests")
def user_service_test_examples() -> str:
    """Example integration tests for the User Service API"""
    return """# User Service Integration Test Examples

## Example 1: Create User - Happy Path

```python
import pytest
import requests

def test_create_user_success():
    # Arrange
    payload = {
        "email": "newuser@example.com",
        "username": "newuser123",
        "firstName": "Jane",
        "lastName": "Smith",
        "role": "user"
    }
    
    # Act
    response = requests.post(
        "https://api.yourapp.com/v1/users",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["username"] == payload["username"]
    assert data["firstName"] == payload["firstName"]
    assert data["lastName"] == payload["lastName"]
    assert data["role"] == "user"
    assert data["isActive"] == True
    assert "id" in data
    assert "createdAt" in data
    assert "updatedAt" in data
```

## Example 2: Create User - Validation Error

```python
def test_create_user_invalid_email():
    # Arrange
    payload = {
        "email": "invalid-email",  # Invalid format
        "username": "testuser",
        "firstName": "Test",
        "lastName": "User"
    }
    
    # Act
    response = requests.post(
        "https://api.yourapp.com/v1/users",
        json=payload
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert "email" in data["error"].lower()
```

## Example 3: Create User - Duplicate Email

```python
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

## Example 4: Update User

```python
def test_update_user():
    # Arrange - Create a user first
    create_payload = {
        "email": "updateme@example.com",
        "username": "updateuser",
        "firstName": "Original",
        "lastName": "Name"
    }
    create_response = requests.post(
        "https://api.yourapp.com/v1/users",
        json=create_payload
    )
    user_id = create_response.json()["id"]
    
    # Act - Update the user
    update_payload = {
        "firstName": "Updated",
        "lastName": "NewName"
    }
    response = requests.patch(
        f"https://api.yourapp.com/v1/users/{user_id}",
        json=update_payload
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["firstName"] == "Updated"
    assert data["lastName"] == "NewName"
    assert data["email"] == create_payload["email"]  # Unchanged
```

## Testing Best Practices

1. **Always clean up test data** - Delete test users after tests
2. **Use unique identifiers** - Add timestamps or UUIDs to test data
3. **Test edge cases** - Empty strings, very long strings, special characters
4. **Test authentication** - Include valid/invalid auth tokens if applicable
5. **Check response headers** - Content-Type, Location, etc.
"""


@mcp.resource("testing://guidelines/integration-tests")
def integration_testing_guidelines() -> str:
    """Best practices and guidelines for writing integration tests"""
    return """# Integration Testing Guidelines

## Test Structure (AAA Pattern)

All integration tests should follow the Arrange-Act-Assert pattern:

1. **Arrange**: Set up test data, prepare payloads
2. **Act**: Execute the API call
3. **Assert**: Verify the response

## What to Test

### 1. Happy Path Scenarios
- Valid inputs produce expected outputs
- Successful status codes (200, 201, 204)
- Response contains all required fields
- Data types match schema

### 2. Validation Errors
- Missing required fields
- Invalid data formats
- Out-of-range values
- Invalid enum values

### 3. Business Logic Errors
- Duplicate records (409 Conflict)
- Invalid state transitions
- Permission violations (403 Forbidden)
- Resource not found (404)

### 4. Edge Cases
- Empty strings
- Maximum length strings
- Special characters
- Null vs undefined values

## Assertion Checklist

For every integration test, verify:
- ✅ HTTP status code
- ✅ Response body structure
- ✅ Required fields are present
- ✅ Data types are correct
- ✅ Values match expected results
- ✅ Error messages are descriptive (for error cases)

## Test Data Management

- Use unique identifiers for each test run
- Clean up test data after tests complete
- Don't rely on existing data - create what you need
- Use fixtures or factories for common test data

## Common Mistakes to Avoid

❌ Hard-coding IDs from production data
❌ Not cleaning up test data
❌ Testing multiple things in one test
❌ Not testing error scenarios
❌ Ignoring response headers
❌ Not verifying all response fields
"""


# TOOLS - Help generate and validate tests
@mcp.tool()
def generate_test_payload(endpoint: str, scenario: str) -> dict:
    """
    Generate a sample API payload for testing
    
    Args:
        endpoint: The API endpoint (e.g., "POST /users", "PATCH /users/{id}")
        scenario: The test scenario (e.g., "valid", "missing_email", "invalid_format")
    
    Returns:
        Sample payload dictionary for the specified scenario
    """
    payloads = {
        "POST /users": {
            "valid": {
                "email": "testuser@example.com",
                "username": "testuser123",
                "firstName": "Test",
                "lastName": "User",
                "role": "user"
            },
            "missing_email": {
                "username": "testuser123",
                "firstName": "Test",
                "lastName": "User"
            },
            "invalid_email": {
                "email": "not-an-email",
                "username": "testuser123",
                "firstName": "Test",
                "lastName": "User"
            },
            "invalid_username": {
                "email": "test@example.com",
                "username": "ab",  # Too short
                "firstName": "Test",
                "lastName": "User"
            }
        },
        "PATCH /users/{id}": {
            "valid": {
                "firstName": "Updated",
                "lastName": "Name"
            },
            "change_role": {
                "role": "admin"
            },
            "deactivate": {
                "isActive": False
            }
        }
    }
    
    endpoint_key = endpoint.split("?")[0]  # Remove query params if any
    if endpoint_key in payloads and scenario in payloads[endpoint_key]:
        return {
            "endpoint": endpoint,
            "scenario": scenario,
            "payload": payloads[endpoint_key][scenario]
        }
    
    return {
        "error": f"No payload template found for endpoint '{endpoint}' and scenario '{scenario}'",
        "available_endpoints": list(payloads.keys()),
        "available_scenarios": list(payloads.get(endpoint_key, {}).keys())
    }


@mcp.tool()
def validate_test_assertions(endpoint: str, response_status: int) -> dict:
    """
    Get recommended assertions for a given endpoint and response status
    
    Args:
        endpoint: The API endpoint being tested
        response_status: The HTTP status code received
    
    Returns:
        Dictionary of recommended assertions to include in the test
    """
    assertions = {
        "POST /users": {
            201: {
                "status_code": "assert response.status_code == 201",
                "required_fields": [
                    "assert 'id' in data",
                    "assert 'email' in data",
                    "assert 'username' in data",
                    "assert 'createdAt' in data",
                    "assert 'updatedAt' in data"
                ],
                "field_values": [
                    "assert data['email'] == payload['email']",
                    "assert data['username'] == payload['username']",
                    "assert data['isActive'] == True"
                ],
                "data_types": [
                    "assert isinstance(data['id'], str)",
                    "assert isinstance(data['isActive'], bool)"
                ]
            },
            400: {
                "status_code": "assert response.status_code == 400",
                "error_response": [
                    "assert 'error' in data",
                    "assert len(data['error']) > 0"
                ]
            },
            409: {
                "status_code": "assert response.status_code == 409",
                "error_response": [
                    "assert 'error' in data",
                    "assert 'already exists' in data['error'].lower()"
                ]
            }
        },
        "GET /users/{id}": {
            200: {
                "status_code": "assert response.status_code == 200",
                "required_fields": [
                    "assert 'id' in data",
                    "assert 'email' in data",
                    "assert 'username' in data"
                ]
            },
            404: {
                "status_code": "assert response.status_code == 404",
                "error_response": [
                    "assert 'error' in data",
                    "assert 'not found' in data['error'].lower()"
                ]
            }
        }
    }
    
    endpoint_key = endpoint.split("?")[0]
    if endpoint_key in assertions and response_status in assertions[endpoint_key]:
        return {
            "endpoint": endpoint,
            "status_code": response_status,
            "assertions": assertions[endpoint_key][response_status]
        }
    
    return {
        "error": f"No assertions found for endpoint '{endpoint}' with status {response_status}",
        "available_endpoints": list(assertions.keys())
    }


@mcp.prompt()
def qa_testing_assistant() -> str:
    """Prompt for helping QA testers learn to write integration tests"""
    return """You are a QA Testing Assistant specialized in helping new QA engineers and developers learn how to write integration tests for APIs.

**Your Expertise:**
- Writing integration tests using Python and pytest
- API testing best practices
- Understanding API schemas and payloads
- Debugging test failures
- Test data management

**Your Capabilities:**
You have access to:
1. API schemas and documentation (via resources)
2. Example integration tests (via resources)
3. Testing guidelines and best practices (via resources)
4. Tools to generate test payloads
5. Tools to validate test assertions

**How to Help Users:**

1. **When asked about an API endpoint:**
   - Reference the API schema resource to explain the endpoint
   - Show the request/response format
   - Explain validation rules

2. **When asked to write a test:**
   - Use the test examples as templates
   - Generate appropriate payloads using the generate_test_payload tool
   - Include all necessary assertions using the validate_test_assertions tool
   - Follow the AAA pattern (Arrange-Act-Assert)
   - Add explanatory comments

3. **When reviewing tests:**
   - Check against the testing guidelines
   - Verify all assertions are present
   - Suggest edge cases to test
   - Recommend best practices

**Response Format:**
- Provide complete, runnable test code
- Include imports and setup
- Add comments explaining each section
- Show expected output or results
- Suggest additional test scenarios

Always be educational and explain WHY you're recommending specific test approaches."""


def main():
    """Entry point for the app-testing-assistant MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
