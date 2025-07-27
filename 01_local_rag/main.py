"""
This script demonstrates how to implement full local RAG (Retrieval-Augmented Generation) setup.
It includes loading documents, splitting them into chunks, creating an embedding store,
and generating responses based on user queries.
"""
import json
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.text import TextLoader
from langchain_ollama import OllamaEmbeddings, ChatOllama
from dotenv import load_dotenv

load_dotenv()

OLLAMA_MODEL_NAME = "llama3.2"  # Ollama model for chat
OLLAMA_EMBEDDING_MODEL_NAME = "all-minilm"  # Ollama model for embeddings
CONTENT_FILE_PATH = "./context.txt"  # Path to the text file containing context

def split_documents(documents: list[Document], chunk_size=200, chunk_overlap=20) -> list[Document]:
    """Split documents into smaller chunks for processing."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, add_start_index=True
    )
    return text_splitter.split_documents(documents)

def split_family_documents(documents: list[Document]) -> list[Document]:
    """Custom function for smarter split of family member documents."""
    member_docs = []
    for family_doc in documents:
        json_data = json.loads(family_doc.page_content)
        family_members = json_data["family_members"]
        for member in family_members:
            member_doc = Document(
                page_content=json.dumps(member, ensure_ascii=False),
                metadata={"source": family_doc.metadata.get("source", "unknown")}
            )
            member_docs.append(member_doc)

    return member_docs

def main():
    """Main function to set up the local RAG system and process user queries."""
    # Create the embedding model and store
    embedding_model = OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL_NAME)
    embedding_store = InMemoryVectorStore(embedding_model)

    # Load documents and split them into manageable chunks
    context_docs = TextLoader(CONTENT_FILE_PATH).load()
    chunks = split_documents(context_docs)

    # Add the document chunks to the embedding store
    # Note: This step transform each chunk into a vector representation.
    embedding_store.add_documents(chunks)

    # Get a query from the user
    query = input("Enter your query: ")

    # Retrieve relevant documents based on the query
    # Note: This step transforms the query into a vector to retrieve similar documents.
    print("\n\nRetrieving relevant documents...")
    relevant_docs = embedding_store.similarity_search(query, k=3)
    
    print("\n\nRelevant documents content:")
    relevant_docs_content = [doc.page_content for doc in relevant_docs]
    for doc in relevant_docs_content:
        print(doc[:100] + "...")
        print(10 * "-")

    # Generate a response using the chat model
    prompt = f"""
        Answer user question based on the context provided. 
        
        <CONTEXT>
        {relevant_docs_content}
        </CONTEXT>

        <USER_QUESTION>
        {query}
        </USER_QUESTION>
        """

    print("\n\nGenerating response...")
    chat_model = ChatOllama(model=OLLAMA_MODEL_NAME)
    response = chat_model.invoke(prompt)

    print("\n\nResponse:", response.content)

if __name__ == "__main__":
    main()
