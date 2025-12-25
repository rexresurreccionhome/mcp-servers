# Baker Virtual Assistant MCP Server - Architecture

## System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        User[Home Baker/Chef]
        Claude[Claude Desktop/AI Client]
    end
    
    subgraph "MCP Protocol"
        MCP[MCP Protocol Layer]
    end
    
    subgraph "Baker Virtual Assistant Server"
        FastMCP[FastMCP Server]
        Resources[Resources<br/>Recipes]
        Tools[Tools<br/>Utilities]
        Prompts[Prompts<br/>Master Baker AI]
    end
    
    subgraph "Knowledge Base"
        Recipes[Recipe Database]
        Tips[Baking Tips]
        Conversions[Unit Conversions]
    end
    
    User -->|Baking questions| Claude
    Claude <-->|MCP Messages| MCP
    MCP <-->|Resource/Tool Calls| FastMCP
    FastMCP --> Resources
    FastMCP --> Tools
    FastMCP --> Prompts
    
    Resources --> Recipes
    Tools --> Tips
    Tools --> Conversions
```

## Component Architecture

```mermaid
graph TD
    subgraph "Server Components"
        Main[main.py]
    end
    
    subgraph "Resources - Recipe Library"
        R1[recipe://banana-loaf<br/>Complete Banana Loaf Recipe]
    end
    
    subgraph "Tools - Utilities"
        T1[get_baking_tips<br/>5 essential tips]
        T2[convert_temperature<br/>F to C converter]
    end
    
    subgraph "Prompts - AI Personality"
        P1[baker_virtual_assistant<br/>Master Baker persona<br/>Scope boundaries]
    end
    
    Main --> R1
    Main --> T1
    Main --> T2
    Main --> P1
```

## User Interaction Flow - Recipe Request

```mermaid
sequenceDiagram
    participant User as Home Baker
    participant Claude
    participant MCP as Baker Assistant
    participant KB as Recipe Library
    
    User->>Claude: "How do I make banana loaf?"
    Claude->>MCP: Request resource: recipe://banana-loaf
    MCP->>KB: Retrieve recipe
    KB-->>MCP: Complete recipe with instructions
    MCP-->>Claude: Recipe content
    Claude-->>User: Formatted recipe with ingredients & steps
    
    User->>Claude: "What temperature in Celsius?"
    Claude->>MCP: convert_temperature(350)
    MCP-->>Claude: {fahrenheit: 350, celsius: 176.67}
    Claude-->>User: "350°F is about 177°C"
```

## User Interaction Flow - Baking Advice

```mermaid
sequenceDiagram
    participant User as Home Baker
    participant Claude
    participant MCP as Baker Assistant
    participant Prompt as Master Baker Prompt
    
    User->>Claude: "Why is my bread dense?"
    Claude->>MCP: Load prompt: baker_virtual_assistant
    MCP->>Prompt: Apply prompt template
    Prompt-->>Claude: Master Baker persona + guidelines
    
    Claude->>MCP: get_baking_tips()
    MCP-->>Claude: 5 essential baking tips
    
    Claude-->>User: Detailed explanation about overmixing,<br/>yeast, kneading + tips + sources
    
    User->>Claude: "What's the weather like?"
    Claude->>Prompt: Check scope boundaries
    Prompt-->>Claude: NOT baking-related
    Claude-->>User: "Sorry I do not understand the question"
```

## Tool Flow - Temperature Conversion

```mermaid
flowchart TD
    Start([User needs temperature]) --> Input[Input: Fahrenheit value]
    Input --> Convert[Calculate: celsius = f - 32 × 5/9]
    Convert --> Round[Round to 2 decimal places]
    Round --> Format[Format response object]
    Format --> Return[Return: fahrenheit & celsius]
    Return --> End([Display to user])
    
    Example[Example: 350°F]
    Example -.-> Convert
    Convert -.-> Result[Result: 176.67°C]
```

## Prompt Flow - Scope Enforcement

```mermaid
flowchart TD
    Question([User Question]) --> Prompt[baker_virtual_assistant prompt]
    Prompt --> Check{Is question<br/>baking-related?}
    
    Check -->|Yes| Process[Process as Master Baker]
    Process --> Research[Use tools & resources]
    Research --> Respond[Detailed baking response]
    Respond --> Format[Add summary + sources]
    Format --> Success([Expert baking advice])
    
    Check -->|No| Reject[Apply boundary rule]
    Reject --> Sorry([Sorry I do not understand<br/>the question])
    
    subgraph "Baking Topics"
        B1[Recipes]
        B2[Techniques]
        B3[Ingredients]
        B4[Equipment]
        B5[Troubleshooting]
    end
    
    Check -.-> B1
    Check -.-> B2
    Check -.-> B3
    Check -.-> B4
    Check -.-> B5
```

## Recipe Resource Structure

```mermaid
graph TD
    Recipe[Banana Loaf Recipe]
    
    Recipe --> Meta[Metadata]
    Meta --> Yield[Yield: 1 loaf, 8-10 slices]
    Meta --> Time[Time: 1h 20m total]
    
    Recipe --> Ing[Ingredients]
    Ing --> Dry[Dry Ingredients<br/>flour, baking soda, salt, cinnamon]
    Ing --> Wet[Wet Ingredients<br/>bananas, sugar, butter, eggs, vanilla]
    Ing --> Optional[Optional Add-ins<br/>nuts, chocolate chips]
    
    Recipe --> Steps[Instructions]
    Steps --> S1[Step 1: Prepare oven & pan]
    Steps --> S2[Step 2: Combine dry ingredients]
    Steps --> S3[Step 3: Mix wet ingredients]
    Steps --> S4[Step 4: Combine wet & dry]
    Steps --> S5[Step 5: Bake 55-65 min]
    Steps --> S6[Step 6: Cool]
    
    Recipe --> Temp[Baking Details]
    Temp --> T1[Temperature: 350°F / 175°C]
    Temp --> T2[Duration: 55-65 minutes]
    Temp --> T3[Test: Toothpick comes clean]
    
    Recipe --> Tips[Tips for Success]
    Tips --> Tip1[Use very ripe bananas]
    Tips --> Tip2[Don't overmix]
    Tips --> Tip3[Check early at 55 min]
    Tips --> Tip4[Room temp ingredients]
    Tips --> Tip5[Tent with foil if browning]
    
    Recipe --> Storage[Storage Instructions]
    Storage --> Room[Room temp: 3 days]
    Storage --> Fridge[Refrigerator: 1 week]
    Storage --> Freeze[Freezer: 3 months]
    
    Recipe --> Vars[Variations]
    Vars --> Choc[Chocolate Banana Loaf]
    Vars --> Nutty[Nutty Banana Loaf]
    Vars --> Trop[Tropical Banana Loaf]
```

## Response Format Workflow

```mermaid
flowchart TD
    Question([Baking Question]) --> Answer[Generate Answer]
    
    Answer --> Content[Main Content<br/>Step-by-step instructions]
    Content --> Summary[Add Concise Summary]
    Summary --> Sources[Add Sources/References]
    Sources --> Format([Final Response])
    
    subgraph "Response Structure"
        P1[Detailed Instructions]
        P2[--- separator ---]
        P3[Summary of Key Points]
        P4[Sources/References]
    end
    
    Format -.-> P1
    Format -.-> P2
    Format -.-> P3
    Format -.-> P4
    
    Example[Example:<br/>Q: Why use room temp butter?]
    Example -.-> E1[A: Room temperature butter<br/>mixes more evenly...]
    E1 -.-> E2[Summary: Room temp ingredients<br/>blend better for even texture]
    E2 -.-> E3[Source: Professional<br/>baking standards]
```

## Data Flow - Recipe Retrieval

```mermaid
flowchart LR
    Request[User: How to make banana loaf?] --> Claude[Claude interprets]
    Claude --> Identify[Identifies: recipe://banana-loaf]
    Identify --> Fetch[Fetch resource]
    Fetch --> Parse[Parse recipe content]
    
    Parse --> Format[Format for readability]
    Format --> Present[Present to user]
    
    subgraph "Recipe Content"
        RC1[Yield & Time]
        RC2[Ingredients List]
        RC3[Step-by-step Instructions]
        RC4[Baking Temperature]
        RC5[Tips & Variations]
    end
    
    Parse --> RC1
    Parse --> RC2
    Parse --> RC3
    Parse --> RC4
    Parse --> RC5
```

## Scope Boundary System

```mermaid
graph TD
    Input([User Input]) --> Parse{Parse Intent}
    
    Parse -->|Baking| In[In Scope]
    Parse -->|Cooking| Out[Out of Scope]
    Parse -->|General| Out
    Parse -->|Other| Out
    
    In --> Categories{Topic Category}
    
    Categories -->|Recipe| Recipe[Provide recipe resource]
    Categories -->|Technique| Tech[Explain technique + tips]
    Categories -->|Ingredient| Ingred[Ingredient info + substitutes]
    Categories -->|Equipment| Equip[Equipment recommendations]
    Categories -->|Troubleshoot| Trouble[Diagnose & solve]
    Categories -->|Temperature| Temp[Convert temperature]
    
    Recipe --> Respond[Detailed Response]
    Tech --> Respond
    Ingred --> Respond
    Equip --> Respond
    Trouble --> Respond
    Temp --> Respond
    
    Out --> Reject[Sorry I do not understand<br/>the question]
    
    subgraph "In Scope Topics"
        IS1[Baking bread, cakes, pastries]
        IS2[Baking techniques & methods]
        IS3[Baking ingredients]
        IS4[Baking equipment]
        IS5[Temperature conversions for baking]
        IS6[Baking troubleshooting]
    end
    
    subgraph "Out of Scope"
        OS1[Cooking non-baked food]
        OS2[Weather, sports, news]
        OS3[General knowledge]
        OS4[Programming, math]
    end
```

## Key Design Decisions

### 1. **Strict Scope Boundaries**
- **Why**: Keeps assistant focused on its expertise (baking)
- **How**: Prompt enforces rejection of non-baking questions
- **Benefit**: Clear value proposition, no scope creep

### 2. **Resource-Based Recipes**
- **Why**: Recipes are static, reusable content
- **How**: Stored as MCP resources with URI scheme `recipe://`
- **Benefit**: Easy to expand recipe library, efficient for LLM context

### 3. **Simple, Practical Tools**
- `get_baking_tips`: Quick reference for common advice
- `convert_temperature`: Solves common F/C conversion need
- **Benefit**: Tools are immediately useful, low complexity

### 4. **Educational Response Format**
```
[Detailed Answer with step-by-step instructions]

Summary:
- Key point 1
- Key point 2

Source: Professional baking standards
```

### 5. **User Persona**
- **Target**: Home bakers and amateur chefs
- **Need**: Reliable recipes, practical advice, conversions
- **Tone**: Expert but approachable, like a master baker mentor

## Extension Possibilities

```mermaid
graph TD
    Current[Current Implementation]
    
    Current --> R1[More Recipes<br/>Bread, cookies, cakes, pastries]
    Current --> R2[More Tools<br/>Weight conversions, timers, scaling]
    Current --> R3[More Features<br/>Dietary substitutions, allergen info]
    Current --> R4[Advanced<br/>Custom recipe creation, meal planning]
    
    R1 --> Growth[Comprehensive Baking Assistant]
    R2 --> Growth
    R3 --> Growth
    R4 --> Growth
    
    Growth --> Future[Future Vision:<br/>Complete digital<br/>baking companion]
```

## Recipe Expansion Model

```mermaid
graph LR
    subgraph "Current Recipes"
        R1[Banana Loaf]
    end
    
    subgraph "Potential Additions"
        Breads[Breads<br/>Sourdough, Focaccia,<br/>Dinner rolls]
        Cakes[Cakes<br/>Chocolate cake,<br/>Cheesecake, Pound cake]
        Cookies[Cookies<br/>Chocolate chip,<br/>Sugar, Oatmeal]
        Pastries[Pastries<br/>Croissants, Scones,<br/>Danishes]
    end
    
    R1 -.->|Same pattern| Breads
    R1 -.->|Same pattern| Cakes
    R1 -.->|Same pattern| Cookies
    R1 -.->|Same pattern| Pastries
```

## Tool Expansion Model

```mermaid
graph TD
    subgraph "Current Tools"
        T1[get_baking_tips]
        T2[convert_temperature]
    end
    
    subgraph "Potential Tools"
        T3[convert_weight<br/>oz to grams]
        T4[scale_recipe<br/>Adjust servings]
        T5[substitute_ingredient<br/>Find alternatives]
        T6[calculate_baking_time<br/>Altitude/pan size]
        T7[check_doneness<br/>Visual/temp guides]
    end
    
    T1 -.->|Similar utility| T3
    T1 -.->|Similar utility| T4
    T2 -.->|Similar utility| T5
    T2 -.->|Similar utility| T6
    T1 -.->|Similar utility| T7
```

## Value Proposition

**For Home Bakers:**
- 🎂 Access to professional-quality recipes
- 🌡️ Quick temperature conversions
- 💡 Expert baking tips on demand
- 🎓 Learn proper techniques with explanations
- ⏱️ Save time with clear instructions

**For Learning:**
- 📚 Understand the "why" behind techniques
- 🔬 Learn baking science
- 🎯 Get troubleshooting help
- 📖 Comprehensive recipe details

## File Structure

```
baker-virtual-assistant/
├── baker_virtual_assistant/
│   ├── __init__.py
│   └── main.py                 # Server implementation
│       ├── Resources (1)       # Banana loaf recipe
│       ├── Tools (2)           # Tips & temperature converter
│       └── Prompts (1)         # Master baker assistant
├── pyproject.toml              # Dependencies
├── README.md                   # Documentation
└── ARCHITECTURE.md             # This file
```

## Implementation Philosophy

### Master Baker Persona

The assistant embodies a **Master Baker** with these characteristics:

1. **Expertise**: Decades of professional baking experience
2. **Teaching Style**: Clear, step-by-step, encouraging
3. **Scope Discipline**: Only answers baking questions
4. **Response Quality**: Always includes summary + sources
5. **Practical Focus**: Prioritizes home bakers' needs

### Response Quality Standards

Every response must:
- ✅ Be relevant to baking
- ✅ Include detailed, actionable instructions
- ✅ Provide a concise summary
- ✅ Cite sources or references
- ✅ Use clear, accessible language
- ❌ Never answer non-baking questions
