from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from backend.tools import query_medgemma

@tool
def mental_support(query: str) -> str:
    return query_medgemma(query)

llm = ChatOllama(model="llama3.1:8b", temperature=0.7)

SYSTEM_PROMPT = """
You are Cortax.
You provide emotional support.
You NEVER claim emergency services were contacted.
"""

def run_agent(user_input: str):
    agent = create_agent(llm, [mental_support])
    return agent.invoke({
        "messages": [
            ("system", SYSTEM_PROMPT),
            ("user", user_input)
        ]
    })
