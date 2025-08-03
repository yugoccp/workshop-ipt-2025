"""
This script demonstrates how memory works in LLMs applications.
"""
from langchain_ollama import ChatOllama

OLLAMA_MODEL_NAME = "llama3.2"  # Ollama model for chat

def main():
    """Main function to demonstrate memory in LLMs."""

    chat_memory = []

    # Get a message from the user
    user_message = input("Enter your query (or press Enter to exit): ")

    while user_message.strip():

        # Store the user message in memory
        chat_memory.append({"content": user_message, "type": "user"})

        # Generate a response using the chat model
        print("\nGenerating response for messages...")
        for msg in chat_memory:
            print(f"[{msg['type']}] {msg['content']}")
            print(10*"-")
            
        chat_model = ChatOllama(model=OLLAMA_MODEL_NAME)
        response = chat_model.invoke(chat_memory)
        
        print("\nResponse:", response.content)

        # Store the response in memory
        chat_memory.append({"content": response.content, "type": "assistant"})

        # Get the next message from the user
        user_message = input("\nEnter your query (or press Enter to exit): ")


if __name__ == "__main__":
    main()
