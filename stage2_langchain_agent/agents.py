from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from tools import get_current_time, read_notes

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

tools = [
    get_current_time,
    read_notes
]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a helpful assistant."
)

print("\nAI Agent (Stage 2 - LangChain Agent)")
print("Type 'exit' to quit\n")

while True:
    user_input = input("User: ")

    if user_input.lower() == "exit":
        break

    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]}
    )

    print("LLM:", response["messages"][-1].content)
    print()