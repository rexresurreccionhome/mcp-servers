# App Testing Assistant MCP Server - Architecture

## System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        QA[QA Engineer/Developer]
        Claude[Claude Desktop/AI Client]
    end
    
    subgraph "MCP Protocol"
        MCP[MCP Protocol Layer]
    end
    
    subgraph "App Testing Assistant Server"
        FastMCP[FastMCP Server]
        Resources[Resources<br/>API Docs & Examples]
        Tools[Tools<br/>Test Generators]
        Prompts[Prompts<br/>QA Assistant]
    end
    
    subgraph "Knowledge Base"
        APISchema[User Service API Schema]
        TestExamples[Integration Test Examples]
        Guidelines[Testing Best Practices]
    end
    
    QA -->|Ask questions| Claude
    Claude <-->|MCP Messages| MCP
    MCP <-->|Resource/Tool Calls| FastMCP
    FastMCP --> Resources
    FastMCP --> Tools
    FastMCP --> Prompts
    
    Resources --> APISchema
    Resources --> TestExamples
    Resources --> Guidelines
```

## Component Architecture

```mermaid
graph TD
    subgraph "Server Components"
        Main[main.py]
    end
    
    subgraph "Resources - Knowledge Base"
        R1[api://schema/user-service<br/>Complete API Documentation]
        R2[api://examples/user-service-tests<br/>Test Code Examples]
        R3[testing://guidelines/integration-tests<br/>Best Practices]
    end
    
    subgraph "Tools - Code Generation"
        T1[generate_test_payload<br/>Create sample payloads]
        T2[validate_test_assertions<br/>Suggest assertions]
    end
    
    subgraph "Prompts - AI Behavior"
        P1[qa_testing_assistant<br/>Specialized QA tutor prompt]
    end
    
    Main --> R1
    Main --> R2
    Main --> R3
    Main --> T1
    Main --> T2
    Main --> P1
```

## User Interaction Flow

```mermaid
sequenceDiagram
    participant QA as QA Engineer
    participant Claude
    participant MCP as Testing Assistant
    participant KB as Knowledge Base
    
    QA->>Claude: "How do I test the POST /users endpoint?"
    Claude->>MCP: Request resource: api://schema/user-service
    MCP->>KB: Retrieve API schema
    KB-->>MCP: Return schema documentation
    MCP-->>Claude: API documentation
    
    Claude->>MCP: Request resource: api://examples/user-service-tests
    MCP->>KB: Retrieve test examples
    KB-->>MCP: Return example tests
    MCP-->>Claude: Test examples
    
    Claude->>MCP: generate_test_payload("POST /users", "valid")
    MCP-->>Claude: Sample payload
    
    Claude->>MCP: validate_test_assertions("POST /users", 201)
    MCP-->>Claude: Recommended assertions
    
    Claude-->>QA: Complete test code with explanations
```

## Tool Flow - Generate Test Payload

```mermaid
flowchart TD
    Start([User: Generate test payload]) --> Input{Parse Input}
    Input -->|endpoint & scenario| Lookup[Lookup in Payload Templates]
    
    Lookup --> Found{Template Exists?}
    
    Found -->|Yes| Extract[Extract Payload for Scenario]
    Extract --> Return[Return Payload JSON]
    
    Found -->|No| Error[Return Error with Available Options]
    
    Return --> End([Response to User])
    Error --> End
    
    subgraph "Payload Templates"
        POST[POST /users<br/>- valid<br/>- missing_email<br/>- invalid_email<br/>- invalid_username]
        PATCH[PATCH /users/{id}<br/>- valid<br/>- change_role<br/>- deactivate]
    end
    
    Lookup -.-> POST
    Lookup -.-> PATCH
```

## Tool Flow - Validate Test Assertions

```mermaid
flowchart TD
    Start([User: Validate assertions]) --> Input{Parse Input}
    Input -->|endpoint & status code| Lookup[Lookup in Assertions Map]
    
    Lookup --> Found{Assertions Exist?}
    
    Found -->|Yes| Categories[Organize by Category]
    Categories --> Status[Status Code Assertion]
    Categories --> Fields[Required Fields Checks]
    Categories --> Values[Field Value Assertions]
    Categories --> Types[Data Type Validations]
    
    Status --> Return[Return All Assertions]
    Fields --> Return
    Values --> Return
    Types --> Return
    
    Found -->|No| Error[Return Error with Available Options]
    
    Return --> End([Response to User])
    Error --> End
    
    subgraph "Assertion Categories"
        C1[Status Code]
        C2[Required Fields]
        C3[Field Values]
        C4[Data Types]
        C5[Error Messages]
    end
    
    Categories -.-> C1
    Categories -.-> C2
    Categories -.-> C3
    Categories -.-> C4
    Categories -.-> C5
```

## Learning Journey Flow

```mermaid
flowchart LR
    subgraph "Phase 1: Discovery"
        A1[Learn API Structure]
        A2[Understand Endpoints]
        A3[Review Request/Response]
    end
    
    subgraph "Phase 2: Examples"
        B1[Study Test Examples]
        B2[Learn AAA Pattern]
        B3[Understand Assertions]
    end
    
    subgraph "Phase 3: Practice"
        C1[Generate Payloads]
        C2[Get Assertion Suggestions]
        C3[Write First Test]
    end
    
    subgraph "Phase 4: Mastery"
        D1[Test Edge Cases]
        D2[Handle Errors]
        D3[Follow Best Practices]
    end
    
    A1 --> A2 --> A3 --> B1
    B1 --> B2 --> B3 --> C1
    C1 --> C2 --> C3 --> D1
    D1 --> D2 --> D3
```

## Resource Data Structure

```mermaid
graph TD
    subgraph "API Schema Resource"
        Schema[API Schema]
        Schema --> Endpoints[Endpoints]
        Endpoints --> POST[POST /users]
        Endpoints --> GET[GET /users/{id}]
        Endpoints --> PATCH[PATCH /users/{id}]
        Endpoints --> DELETE[DELETE /users/{id}]
        
        POST --> ReqFormat[Request Format]
        POST --> ResFormat[Response Format]
        POST --> Validation[Validation Rules]
        POST --> Errors[Error Codes]
    end
    
    subgraph "Test Examples Resource"
        Examples[Test Examples]
        Examples --> Happy[Happy Path Tests]
        Examples --> Invalid[Validation Error Tests]
        Examples --> Conflict[Duplicate Data Tests]
        Examples --> Update[Update Operation Tests]
        
        Happy --> AAA[AAA Pattern]
        AAA --> Arrange
        AAA --> Act
        AAA --> Assert
    end
    
    subgraph "Guidelines Resource"
        Guide[Testing Guidelines]
        Guide --> Structure[Test Structure]
        Guide --> WhatTest[What to Test]
        Guide --> Checklist[Assertion Checklist]
        Guide --> DataMgmt[Test Data Management]
        Guide --> Mistakes[Common Mistakes]
    end
```

## Test Generation Workflow

```mermaid
sequenceDiagram
    participant QA as QA Engineer
    participant Claude
    participant Assistant as Testing Assistant
    participant Templates as Template Store
    
    QA->>Claude: "Generate a test for creating a user with invalid email"
    
    Claude->>Assistant: Get API schema
    Assistant-->>Claude: POST /users endpoint details
    
    Claude->>Assistant: generate_test_payload("POST /users", "invalid_email")
    Assistant->>Templates: Lookup payload template
    Templates-->>Assistant: Invalid email payload
    Assistant-->>Claude: {"email": "not-an-email", ...}
    
    Claude->>Assistant: validate_test_assertions("POST /users", 400)
    Assistant->>Templates: Lookup assertion templates
    Templates-->>Assistant: 400 error assertions
    Assistant-->>Claude: [status check, error field checks]
    
    Claude->>Claude: Combine: schema + payload + assertions + AAA pattern
    Claude-->>QA: Complete test code with comments
```

## Key Design Decisions

### 1. **Resource-Based Knowledge Sharing**
- API schemas as resources provide complete documentation context
- Test examples as resources show real-world patterns
- Guidelines as resources teach best practices
- LLM can reference all materials when answering questions

### 2. **Tool-Based Code Generation**
- `generate_test_payload`: Reduces boilerplate, ensures consistency
- `validate_test_assertions`: Teaches what to verify in tests
- Template-based approach allows easy expansion

### 3. **Prompt Engineering**
- Specialized QA testing assistant prompt sets clear role boundaries
- Instructs how to use resources and tools effectively
- Emphasizes educational approach with explanations

### 4. **Testing Philosophy (AAA Pattern)**
```python
# Arrange: Set up test data
payload = {...}

# Act: Execute API call
response = requests.post(url, json=payload)

# Assert: Verify results
assert response.status_code == 201
```

### 5. **Coverage Areas**
- ✅ Happy path scenarios (201, 200 responses)
- ✅ Validation errors (400 responses)
- ✅ Business logic conflicts (409 responses)
- ✅ Resource not found (404 responses)
- ✅ Edge cases and data types

## Supported API Endpoints

```mermaid
graph LR
    API[User Service API]
    
    API --> Create[POST /users<br/>Create new user]
    API --> Read[GET /users/{id}<br/>Get user details]
    API --> Update[PATCH /users/{id}<br/>Update user]
    API --> Delete[DELETE /users/{id}<br/>Soft delete user]
    
    Create --> C1[201: Success]
    Create --> C2[400: Validation Error]
    Create --> C3[409: Duplicate]
    
    Read --> R1[200: Success]
    Read --> R2[404: Not Found]
    Read --> R3[403: Forbidden]
    
    Update --> U1[200: Success]
    Update --> U2[400: Invalid Data]
    Update --> U3[404: Not Found]
    Update --> U4[409: Conflict]
    
    Delete --> D1[204: No Content]
    Delete --> D2[404: Not Found]
    Delete --> D3[409: Cannot Delete]
```

## Extension Points

```mermaid
graph TD
    Current[Current Implementation]
    
    Current --> E1[Add More Endpoints<br/>Orders, Products, etc.]
    Current --> E2[Add More Test Scenarios<br/>Performance, Security]
    Current --> E3[Add More Languages<br/>JavaScript, Java]
    Current --> E4[Add Test Execution<br/>Run tests directly]
    Current --> E5[Add CI/CD Integration<br/>GitHub Actions examples]
    
    E1 --> Growth[Expanded Testing Assistant]
    E2 --> Growth
    E3 --> Growth
    E4 --> Growth
    E5 --> Growth
```

## File Structure

```
app-testing-assistant/
├── app_testing_assistant/
│   ├── __init__.py
│   └── main.py                 # Server implementation
│       ├── Resources (3)       # API docs, examples, guidelines
│       ├── Tools (2)           # Payload & assertion generators
│       └── Prompts (1)         # QA assistant behavior
├── pyproject.toml              # Dependencies
├── README.md                   # Documentation
└── ARCHITECTURE.md             # This file
```

## Value Proposition

**For QA Engineers:**
- 📚 Learn API structure interactively
- 🎯 Get instant test code examples
- ✅ Ensure complete test coverage
- 🚀 Accelerate test writing

**For Development Teams:**
- 📖 Living API documentation
- 🔄 Consistent testing patterns
- 👥 Faster onboarding
- 🛡️ Higher quality assurance
