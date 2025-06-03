from langchain_core.messages import SystemMessage
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from typing import List, TypedDict
from dotenv import load_dotenv
import asyncio
from base_agent.prompts import call_model_prompt


# MCP Imports
from langchain_mcp_adapters.client import MultiServerMCPClient

# Load environment variables from .env file
load_dotenv()

# --- Define Agent State ---
class AgentState(TypedDict):
    """State for the agent with proper typing for LangSmith Studio"""
    messages: List

# --- MCP Client Setup (used as tool provider) ---
async def get_mcp_tools():
    client = MultiServerMCPClient(
        {        
            "google_calendar": {
                # Write here your Smithery MCP Google Calendar URL after configuration
                "url": "<write your Smithery MCP Google Calendar URL here>",
                "transport": "streamable_http",
            },
        }
    )
    return await client.get_tools()

# Fetch tools synchronously for LangStudio compatibility
mcp_tools = asyncio.run(get_mcp_tools())

# --- Use Only MCP Tools ---
tools = mcp_tools

# --- LLM Setup ---
llm = ChatOpenAI(model="gpt-4o", temperature=0.1)
llm_with_tools = ChatOpenAI(model="gpt-4o", temperature=0.3).bind_tools(tools)

# --- Graph Node Definition ---
def call_model(state: AgentState) -> AgentState:
    response = llm_with_tools.invoke([call_model_prompt] + state["messages"])
    return {"messages": state["messages"] + [response]}

# --- LangGraph Construction ---
builder = StateGraph(MessagesState)
builder.add_node("call_model", call_model)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "call_model")
builder.add_conditional_edges("call_model", tools_condition)
builder.add_edge("tools", "call_model")
graph = builder.compile()
