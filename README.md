# AI Agent Architecture Evolution

This project demonstrates the evolution of AI agent architectures:

1. Basic LLM application
2. LangChain agents with tools
3. LangGraph workflows
4. MCP-based tool infrastructure

---

## Stage 1: Basic LLM Application

Architecture:
User → LangChain → LLM → Response

Purpose:
Understand the fundamental building block of AI applications before introducing tools and agents.

Core concept:
LLM Invocation

Important APIs:
llm.invoke()
---

## Stage 2: Stage-2 Goal

Build a LangChain Agent with Tools

Architecture:
    User
     ↓
    Agent
     ↓
    Tools
     ↓
    Result
    
Agent loop:
    User question
    ↓
    LLM decides action
    ↓
    Call tool
    ↓
    Observe result
    ↓
    Return final answer

Key LangChain concepts:
1. Tool decorator
2. Agent
3. ReAct reasoning
4. Tool invocation

Important APIs:
1. @tool
2. initialize_agent()
3. agent.invoke()


---

## Stage 3: Stage-3 Goal

Upgrade Stage-2 (LangChain agent) into a LangGraph state machine agent.

Architecture:
    User → Agent → Tool → Answer
    
    state graph:
        ┌───────────┐
        │   Start   │
        └─────┬─────┘
              │
        ┌─────▼─────┐
        │    LLM    │
        │ reasoning │
        └─────┬─────┘
              │
        ┌─────▼─────┐
        │ Tool Node │
        └─────┬─────┘
              │
        ┌─────▼─────┐
        │  Final    │
        └───────────┘
        
    LangGraph workflow:
        User question
              │
              ▼
        LLM decides action
              │
              ▼
        Tool execution
              │
              ▼
        LLM observes result
              │
              ▼
        Final answer
    
    
    Reasoning Loop:
        User Question
              │
              ▼
        Agent Node (LLM reasoning)
              │
              ▼
        Tool Call?
              │
         ┌────┴────┐
         │         │
        Yes        No
         │         │
         ▼         ▼
        Tool Node  Final Answer
         │
         ▼
        Agent Node
    
    
    Output:
          START
            │
            ▼
          agent
            │
       ┌────┴─────┐
       │          │
      tools      END
       │
       ▼
      agent
      

Important APIs:
1. StateGraph
2. add_node, set_entry_point, add_conditional_edges, add_edge
3. workflow.compile()
4. graph.invoke()

---

## Stage 4: MCP

Goal

    We move tools outside the agent into an MCP Server.

    Before:
        Agent
         ├─ tool: read_notes()
         ├─ tool: get_time()
         └─ tool: database_query()
         
    After:
        Agent
           │
           ▼
        MCP Client
           │
           ▼
        MCP Server
           ├─ read_notes()
           ├─ get_time()
           └─ database_query()
           
        Agent no longer owns the tools
        
    Without MCP: Every AI system implements tools again
    With MCP: One MCP Server exposes tools. All agents reuse them
    
    