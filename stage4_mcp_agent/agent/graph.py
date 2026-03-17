from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from typing import TypedDict, Annotated
import operator
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

def mcp_tools_to_langchain(mcp_tools) -> list:
    return [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description or f"Tool: {t.name}",
                "parameters": t.inputSchema,
            },
        }
        for t in mcp_tools
    ]


def build_graph(session):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    async def agent_node(state: AgentState):

        # Discover tools from MCP server at runtime
        tools_response = await session.list_tools()

        tools_schema = mcp_tools_to_langchain(tools_response.tools)
        llm_with_tools = llm.bind_tools(tools_schema)

        # Invoke LLM with the full conversation history
        response = await llm_with_tools.ainvoke(state["messages"])

        # Append the LLM response (may be AIMessage with tool_calls, or plain text)
        return {"messages": [response]}

    async def tool_executor_node(state: AgentState):
        last_message = state["messages"][-1]
        tool_messages = []

        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            print(f"  [Executing tool] {tool_name}({tool_args})")

            # Route the call through the live MCP server
            mcp_result = await session.call_tool(tool_name, arguments=tool_args)

            # Extract text result from MCP response
            result_text = (
                mcp_result.content[0].text
                if mcp_result.content
                else "(no result returned)"
            )

            print(f"  [Tool result] {result_text[:120]}")

            tool_messages.append(
                ToolMessage(
                    content=result_text,
                    tool_call_id=tool_call["id"],
                )
            )

        return {"messages": tool_messages}

    def should_continue(state: AgentState) -> str:
        last_message = state["messages"][-1]

        if isinstance(last_message, AIMessage) and last_message.tool_calls:
            return "tool_executor"

        return END

    graph = StateGraph(AgentState)

    graph.add_node("agent", agent_node)
    graph.add_node("tool_executor", tool_executor_node)

    graph.set_entry_point("agent")

    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tool_executor": "tool_executor",
            END: END,
        }
    )

    graph.add_edge("tool_executor", "agent")

    return graph.compile()