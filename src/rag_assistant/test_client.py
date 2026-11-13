import asyncio
import os
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    project_root = Path(__file__).resolve().parents[2]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root / "src")

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "rag_assistant.server"],
        cwd=str(project_root),
        env=env,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Outils disponibles :", tools)
            
            result = await session.call_tool(
            "ask_rag",
            arguments={
                "question": "Quelle est la différence entre un groupe et un corps ?"
            },
            )

            print("Réponse du RAG :")
            print(result.structured_content["result"])


if __name__ == "__main__":
    asyncio.run(main())