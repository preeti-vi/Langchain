from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from dotenv import load_dotenv
load_dotenv()


# Define Add function to use it as a Tool
def add(a: int , b: int) -> int :
    """
    Add a and b
    Args:
        a: first int
        b: second int
    """
    return a + b + 10


# Bind the tool to the LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")
# llm_with_tools = llm.bind_tools([{"title": "Add function", "function": add, "description": "Add 2 numbers"}])  # or add docstring in function
llm_with_tools = llm.bind_tools([add])


# LLM calling Tool node
def llm_calling_tool(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# Build graph
builder = StateGraph(MessagesState)

builder.add_node("llm_calling_tool_node", llm_calling_tool)
builder.add_node("tools", ToolNode([add]))

builder.add_edge(START, "llm_calling_tool_node")
builder.add_conditional_edges("llm_calling_tool_node", tools_condition)
builder.add_edge("tools", END)

graph = builder.compile()

response = graph.invoke({"messages": "What is the addition of 2 and 3, really"})
print(response)

