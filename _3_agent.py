from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv


load_dotenv()


def multiply(a,b):
    """This function multiplies 2 numbers"""
    return a * b

def add(a,b):
    """This function adds 2 numbers"""
    return a + b

def divide(a,b):
    """This function divide first number by the second number"""
    return a / b


# Define the LLM model with tools bind to it
tools = [multiply, add, divide]
llm = ChatOpenAI(model="gpt-3.5-turbo")
llm_with_tools = llm.bind_tools(tools, parallel_tool_calls = False)


# Define a Node function - to invoke llm with tools model
def llm_with_tools_calling(state: MessagesState):
    return {"messages" : llm_with_tools.invoke(state["messages"])}

# Define the graph
builder = StateGraph(MessagesState)

builder.add_node("assistant", llm_with_tools_calling)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools","assistant")

lgraph = builder.compile()

# Define a system prompt

# Define a user prompt
prompt = "Multiply 2 and 4. Add 4 to it. Divide it by 4"

response = lgraph.invoke({"messages" : prompt})
print(f"Response : {response}")

for m in response['messages']:
    m.pretty_print()