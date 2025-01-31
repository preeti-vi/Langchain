from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph.message import add_messages

from dotenv import load_dotenv
load_dotenv()


class MyMessagesState(MessagesState):
    # Add any keys needed beyond messages, which is pre-built
    pass


llm = ChatOpenAI()


# Node
def tool_calling_llm(state: MyMessagesState):
    return {"messages": [llm.invoke(state["messages"])]}


def node_2(state: MyMessagesState):
    return {"messages": [llm.invoke(state["messages"])]}


# Build graph
builder = StateGraph(MyMessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("node_2", node_2)
builder.add_edge(START, "tool_calling_llm")
builder.add_edge("tool_calling_llm","node_2")
builder.add_edge("node_2", END)
graph = builder.compile()

# response = graph.invoke({"messages": HumanMessage(content="Hello!")})
response = graph.invoke({"messages": "I want to test the chain"})
print(response)

# View
# display(Image(graph.get_graph().draw_mermaid_png()))