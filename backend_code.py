from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import logging
import os


def ask_ai_2_queries_in_loop(user_msg):
    load_dotenv()
    logging.basicConfig(level=logging.ERROR)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    logging.error(f"Key is : {OPENAI_API_KEY}")

    llm = ChatOpenAI(model = "gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY, temperature = 0.7, max_tokens=60)

    def llm_calling(state: MessagesState):
        resp = llm.invoke(state["messages"])
        logging.error(resp)
        return {"messages": resp}

    builder = StateGraph(MessagesState)
    builder.add_node("llm_1", llm_calling)
    builder.add_node("llm_2", llm_calling)

    builder.add_edge(START, "llm_1")
    builder.add_edge("llm_1","llm_2")
    builder.add_edge("llm_2", END)

    lgraph = builder.compile()

    response = lgraph.invoke({"messages": user_msg})

    return [m.content for m in response["messages"]]

if __name__ == "__main__":
    res = ask_ai_2_queries_in_loop("I want something new")
    for res_str in res:
        print(res_str)
