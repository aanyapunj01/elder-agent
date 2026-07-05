"""
main.py
--------
CLI demo entry point.
"""

from agents.orchestrator import Orchestrator
from config import MOCK_MODE


def main():
    print("=" * 60)
    print(" Elderly & Disabled Task Automation Assistant (CLI demo)")
    print("=" * 60)
    if MOCK_MODE:
        print("[Running in MOCK MODE — no GEMINI_API_KEY found.]")
        print("[Responses are simplified. Add a key to .env for full LLM behavior.]\n")
    print("Type 'quit' to exit.\n")

    orchestrator = Orchestrator()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in ("quit", "exit"):
            print("Assistant: Take care! I'm always here if you need me.")
            break
        if not user_input:
            continue

        reply = orchestrator.handle_message(user_input)
        print(f"Assistant: {reply}\n")


if __name__ == "__main__":
    main()