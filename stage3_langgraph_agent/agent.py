from dotenv import load_dotenv
from graph import run_agent

print("\nLangGraph Agent (Stage 3)")
print("Type 'exit' to quit\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

    answer = run_agent(question)

    print("\nAI:", answer)
    print()