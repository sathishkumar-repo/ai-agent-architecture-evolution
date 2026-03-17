"""
agent.py — Main Entry Point

Flow

Server -> Agent (LLM) -> Tool Calls -> MCP Session -> Tools -> MCP Session -> Agent (LLM) -> Final Answer

server.py     →  defines what tools CAN do       (capability)
mcp_tools.py  →  opens the pipe to server.py     (connection)
graph.py      →  decides WHEN to call tools      (orchestration)
agent.py      →  ties it together, runs the loop (entry point)

"""

import asyncio
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

from graph import build_graph
from mcp_tools import get_mcp_session

load_dotenv()


async def run():
    print("\n" + "=" * 55)
    print("  AI Agent  —  LangGraph + MCP Tools")
    print("  Tools: get_current_time, read_notes")
    print("  Type 'exit' to quit")
    print("=" * 55)

    async with get_mcp_session() as session:

        app = build_graph(session)

        while True:
            try:
                question = input("\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                break

            if not question:
                continue

            if question.lower() in {"exit", "quit", "q"}:
                print("Goodbye!")
                break

            print("\nThinking...\n")

            # LangGraph expects messages in the state
            # HumanMessage wraps the user's plain text into the LangChain format
            result = await app.ainvoke(
                {"messages": [HumanMessage(content=question)]}
            )

            # The final answer is the content of the last message in the list
            final_message = result["messages"][-1]
            print(f"\nAI: {final_message.content}")


if __name__ == "__main__":
    asyncio.run(run())