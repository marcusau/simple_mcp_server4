from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for hong kong"""
    
    weather={"hongkong":"Sunny","beijing":"Cloudy","shanghai":"Rainy"}
    return f"The weather in {location} is {weather[location]}"

if __name__ == "__main__":
    mcp.run(transport="stdio")