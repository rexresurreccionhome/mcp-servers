from mcp.server.fastmcp import FastMCP

mcp = FastMCP("baker-virtual-assistant")


@mcp.tool()
def get_baking_tips() -> str:
    """Get helpful baking tips and advice"""
    return (
        "Here are some essential baking tips:\n"
        "1. Always measure ingredients accurately\n"
        "2. Preheat your oven before baking\n"
        "3. Room temperature ingredients mix better\n"
        "4. Don't overmix your batter\n"
        "5. Use an oven thermometer for accurate temperature"
    )


@mcp.tool()
def convert_temperature(fahrenheit: float) -> dict:
    """Convert Fahrenheit to Celsius for baking"""
    celsius = (fahrenheit - 32) * 5/9
    return {
        "fahrenheit": fahrenheit,
        "celsius": round(celsius, 2)
    }


@mcp.resource("recipe://banana-loaf")
def banana_loaf_recipe() -> str:
    """Complete recipe for baking a delicious Banana Loaf"""
    return """# Banana Loaf Recipe

## Yield
Makes 1 loaf (8-10 slices)

## Time
- Preparation Time: 15 minutes
- Baking Time: 55-65 minutes
- Total Time: ~1 hour 20 minutes

## Ingredients

### Dry Ingredients:
- 2 cups all-purpose flour (240g / 8.5 oz)
- 1 teaspoon baking soda (5g)
- 1/4 teaspoon salt (1.5g)
- 1/2 teaspoon ground cinnamon (2g) - optional

### Wet Ingredients:
- 3 large ripe bananas, mashed (about 1 1/2 cups / 340g)
- 3/4 cup granulated sugar (150g / 5.3 oz)
- 1/2 cup unsalted butter, melted (115g / 4 oz)
- 2 large eggs, beaten
- 1 teaspoon vanilla extract (5ml)

### Optional Add-ins:
- 1/2 cup chopped walnuts or pecans (60g)
- 1/2 cup chocolate chips (85g)

## Instructions

### Step 1: Prepare
Preheat your oven to 350°F (175°C / Gas Mark 4). Grease a 9x5 inch (23x13 cm) loaf pan with butter or line it with parchment paper.

### Step 2: Combine Dry Ingredients
In a medium bowl, whisk together the flour, baking soda, salt, and cinnamon (if using). Set aside.

### Step 3: Mix Wet Ingredients
In a large mixing bowl, mash the ripe bananas with a fork until smooth with only small lumps remaining. Add the melted butter and stir to combine. Mix in the sugar, beaten eggs, and vanilla extract until well incorporated.

### Step 4: Combine Wet and Dry
Gently fold the dry ingredients into the wet ingredients using a spatula or wooden spoon. Mix until just combined - do not overmix! The batter should be slightly lumpy. If using nuts or chocolate chips, fold them in at this stage.

### Step 5: Bake
Pour the batter into the prepared loaf pan and smooth the top with a spatula. Bake for 55-65 minutes, or until a toothpick inserted into the center comes out clean or with just a few moist crumbs.

### Step 6: Cool
Remove from the oven and let the loaf cool in the pan for 10-15 minutes. Then transfer to a wire rack to cool completely before slicing.

## Baking Temperature & Duration
- Temperature: 350°F (175°C / Gas Mark 4)
- Duration: 55-65 minutes
- Test for doneness: Insert a toothpick in the center - it should come out clean or with a few moist crumbs

## Tips for Success

1. **Use Very Ripe Bananas**: The bananas should be heavily spotted or even black for the best flavor and natural sweetness.

2. **Don't Overmix**: Mix the batter just until the flour is incorporated. Overmixing develops gluten and makes the loaf tough.

3. **Check Early**: Ovens vary, so start checking at 55 minutes. The top should be golden brown and spring back when lightly touched.

4. **Room Temperature Ingredients**: For best results, use eggs at room temperature.

5. **Tent with Foil**: If the top is browning too quickly, loosely cover with aluminum foil for the last 15-20 minutes of baking.

## Storage Instructions
- Room Temperature: Store in an airtight container for up to 3 days
- Refrigerator: Keeps for up to 1 week
- Freezer: Wrap tightly in plastic wrap and aluminum foil, freeze for up to 3 months

## Variations
- **Chocolate Banana Loaf**: Add 1/4 cup cocoa powder to dry ingredients and reduce flour by 1/4 cup
- **Nutty Banana Loaf**: Add 1/2 cup chopped walnuts or pecans
- **Tropical Banana Loaf**: Add 1/2 cup shredded coconut and 1/4 cup chopped macadamia nuts
"""


@mcp.prompt()
def baker_virtual_assistant(user_input: str) -> str:
    """A master baker virtual assistant that provides expert baking advice and instructions"""
    return f"""You are a Master Baker Virtual Assistant with decades of professional baking experience. Your expertise covers all aspects of baking, from bread and pastries to cakes and cookies.

**Your Role and Expertise:**
- You ONLY answer questions related to baking, baked goods, baking techniques, ingredients, equipment, and recipes
- You are a master baker with deep knowledge of the science and art of baking
- You provide clear, step-by-step instructions that are easy to follow for bakers of all skill levels

**Your Boundaries:**
- If a question is NOT related to baking, you MUST respond with: "Sorry I do not understand the question"
- Do not answer questions about cooking (non-baking), other topics, or general knowledge unrelated to baking

**Your Response Format:**
1. Provide detailed, step-by-step instructions when applicable
2. Make your instructions user-friendly and easy to understand
3. At the end of EVERY response, include:
   - A concise summary of the key points
   - Sources or references for the information provided (e.g., "Based on professional baking standards" or "Classic French baking technique")

**User's Question:**
{user_input}

Please provide your expert response following the guidelines above."""


def main():
    """Entry point for the baker-virtual-assistant MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
