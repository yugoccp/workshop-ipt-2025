from pathlib import Path
import kuzu
from langchain_ollama import ChatOllama
import re

GRAPHDB_PATH = Path(__file__).parent.parent / "graphdb"
GRAPHDB_SCHEMA_PATH = GRAPHDB_PATH / "cypher/schema.cypher"
GRAPHDB_DATABASE_PATH = GRAPHDB_PATH / "database/database.kuzu"
OLLAMA_MODEL_NAME = "llama3.2"


def main():
    """Main function to set up the graph database and process user queries."""

    if not GRAPHDB_DATABASE_PATH.exists():
        raise SystemError("Run script `graphdb/init_graphdb.sh` script before running this example.")

    db = kuzu.Database(GRAPHDB_DATABASE_PATH)
    conn = kuzu.Connection(db)

     # Get a message from the user
    user_message = input("\nEnter your query: ")

    # Generate a response using the chat model
    graph_schema = GRAPHDB_SCHEMA_PATH.read_text()
    prompt_cypher = f"""
        You are an expert Neo4j developer. 
        Your task is to generate a syntactically correct Cypher query based on the provided graph schema and user question.
        Return ONLY the cypher query as response.

        <GRAPH_SCHEMA>
        {graph_schema}
        </GRAPH_SCHEMA>

        <USER_QUESTION>
        {user_message}
        </USER_QUESTION>
        """
    
    chat_model = ChatOllama(model=OLLAMA_MODEL_NAME)

    print("\nGenerating Cypher Query...")
    response = chat_model.invoke(prompt_cypher)
    print(response.content)

    # Remove code block markers from the query for clean execution
    cypher_query = re.sub(r"```(?:cypher)?\s*([\s\S]*?)\s*```", r"\1", response.content).strip()
    
    print("\nExecuting Cypher Query...")
    result = conn.execute(cypher_query)
    cypher_results = result.get_all()

    for row in cypher_results:
        print(row)
        print(10 * "-")
    
    prompt_question = f"""
        You are a helpful assistant.
        Answer user questions based ONLY on the QUERY_RESULTS.
        Reply in a concise and natural manner.
        DON'T include query details or database schema on final response.
        
        <QUERY_RESULTS>
        Query: {cypher_query}
        Result: {cypher_results}
        </QUERY_RESULTS>

        <USER_QUESTION>
        {user_message}
        </USER_QUESTION>
        """
    
    print("\nGenerating response...")
    response = chat_model.invoke(prompt_question)

    print("\nResponse:", response.content)

if __name__ == "__main__":
    main()
