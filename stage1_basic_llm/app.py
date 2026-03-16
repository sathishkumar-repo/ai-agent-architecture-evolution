from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

while True:
    user_input = input("User: ")

    if user_input.lower() == 'exit':
        print("Exiting the chat. Goodbye!")
        break
    response = llm.invoke(user_input)

    print(f"LLM: {response.content}")

    print()