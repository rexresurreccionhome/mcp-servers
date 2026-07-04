from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hello-world")


@mcp.tool()
def simple_hello_world_poem() -> str:
    return (
        "Hello, World! A phrase so bright,\n"
        "In coding realms, it sheds its light,\n"
        "A simple start, a coder's friend,\n"
        "From here, the journey has no end."
    )


def main():
    """Entry point for the hello-world MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
