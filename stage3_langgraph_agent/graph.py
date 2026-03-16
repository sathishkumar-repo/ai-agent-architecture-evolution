from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage
from tools import get_current_time, read_notes
from state import AgentState
from dotenv import load_dotenv

load_dotenv()

# Initialize model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

tools = [get_current_time, read_notes]

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)

tool_node = ToolNode(tools)


# Node 1: LLM reasoning
def agent_node(state: AgentState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


# Decision function
def should_continue(state: AgentState):

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tools"

    return END


# Build graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END,
    },
)

workflow.add_edge("tools", "agent")

graph = workflow.compile()

print(graph.get_graph().draw_ascii())

def run_agent(query: str):

    result = graph.invoke(
        {"messages": [HumanMessage(content=query)]}
    )

    return result["messages"][-1].content