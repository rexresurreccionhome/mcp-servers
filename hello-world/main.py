from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hello-world")


@mcp.tool()
def what_is_hello_world() -> str:
    return "Hello World is a simple program that outputs 'Hello, World!' to demonstrate basic syntax."


@mcp.tool()
def simple_hello_world_poem() -> str:
    return (
        "Hello, World! A phrase so bright,\n"
        "In coding realms, it sheds its light,\n"
        "A simple start, a coder's friend,\n"
        "From here, the journey has no end."
    )


if __name__ == "__main__":
    mcp.run()
