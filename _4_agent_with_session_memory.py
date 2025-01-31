from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv


load_dotenv()

# Define the LLM model
llm = ChatOpenAI(model="gpt-3.5-turbo")


# Define a Node function - to invoke llm with tools model
def llm_calling(state: MessagesState):
    return {"messages" : llm.invoke(state["messages"])}


def build_graph(memory_flag : bool):
    builder = StateGraph(MessagesState)

    builder.add_node("simple_agent", llm_calling)

    builder.add_edge(START, "simple_agent")
    builder.add_edge("simple_agent",END)

    if(memory_flag):
        memory = MemorySaver()
        lgraph = builder.compile(checkpointer = memory)
    else:
        lgraph = builder.compile()

    return lgraph


print("*" * 5 + "Call a graph agent without memory" + "*" * 5)

# Create a graph without memory
lgraph = build_graph(memory_flag=False)

# First call
prompt = "My name is ABC"
response = lgraph.invoke({"messages" : prompt})
print(f"Response 1: {response}")

# Second call
prompt = "What is my name?"
response = lgraph.invoke({"messages" : prompt})
print(f"Response 2: {response}")


print("*" * 5 + "Call a graph agent with memory" + "*" * 5)

# Create a graph without memory
lgraph = build_graph(memory_flag=True)

# First call
# Specify a thread
session_id = "1"
session_config_1 = {"configurable": {"thread_id": session_id}}

prompt = "My name is Seema"
response = lgraph.invoke({"messages" : prompt}, config=session_config_1)
print(f"Response 1 for Seema: {response}")

session_id = "2"
session_config_2 = {"configurable": {"thread_id": session_id}}

prompt = "My name is Rahul"
response = lgraph.invoke({"messages" : prompt}, config=session_config_2)
print(f"Response 1 for Rahul: {response}")

# Second call
prompt = "What is my name?"
response = lgraph.invoke({"messages" : prompt}, config=session_config_1)
print(f"Response 2 for Seema: {response}")

prompt = "What is my name?"
response = lgraph.invoke({"messages" : prompt}, config=session_config_2)
print(f"Response 2 for Rahul: {response}")
