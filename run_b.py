# run.py

from openai_agent import call_openai_with_tools

while True:
    user_input = input("🧠 Kaala > ")
    if user_input.lower() in ["exit", "quit"]:
        break
    response = call_openai_with_tools(user_input)
    print("🤖", response)

