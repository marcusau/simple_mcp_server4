import asyncio
from typing import Any, Dict

import dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
load_dotenv()

# model = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

model = ChatOllama(model="llama3.2:3b")


async def invoke_client() -> Dict[str, Any]:
    async with MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["math_server.py"],
                "transport": "stdio",
            },
            "weather": {
                # make sure you start your weather server on port 8000
                # "url": "http://localhost:8000/sse",
                # "transport": "sse",
                "command": "python",
                "args": ["weather_server.py"],
                "transport": "stdio",
            },
        }
    ) as client:
        agent = create_react_agent(model, client.get_tools())
        math_response = await agent.ainvoke({"messages": "Use the math tool to calculate what's (3 + 5) x 12?"})
        weather_response = await agent.ainvoke( {"messages": "use the weather tool to get what is the weather in Beijing?"})
        return {
            "math_response": math_response["messages"][-1].content,
            "weather_response": weather_response["messages"][-1].content,
        }

if __name__ == "__main__":
    answer = asyncio.run(invoke_client())
    print("weather_response:",answer.get("weather_response"))
    print("-"*100)
    print("math_response:",answer.get("math_response"))