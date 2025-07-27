"""
This script demonstrates how memory works in LLMs applications.
"""
from langchain_ollama import ChatOllama

OLLAMA_MODEL_NAME = "llama3.2"  # Ollama model for chat

def main():
    """Main function to demonstrate memory in LLMs."""

    # Get a message from the user
    user_message = input("Enter your query (or press Enter to exit): ")

    while user_message.strip():

        # Generate a response using the chat model
        print("\nGenerating response...")
        chat_model = ChatOllama(model=OLLAMA_MODEL_NAME)
        response = chat_model.invoke(user_message)
        
        print("\nResponse:", response.content)

        # Get the next message from the user
        user_message = input("\nEnter your query (or press Enter to exit): ")


if __name__ == "__main__":
    main()
