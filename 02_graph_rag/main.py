from pathlib import Path
import kuzu
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import JsonOutputParser

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
        Generate cypher query based on graph database schema to support answer the user question.
        Return the query ONLY as a JSON object with the key "cypher".

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

    print("\nExtracting Cypher Query from Response...")
    json_parser = JsonOutputParser()
    json_response = json_parser.parse(text=response.content)
    cypher_query = json_response["cypher"]
    
    print("\nExecuting Cypher Query...")
    result = conn.execute(cypher_query)
    cypher_results = result.get_all()

    for row in cypher_results:
        print(row)
        print(10 * "-")
    
    prompt_question = f"""
        You are a helpful assistant.
        Answer user questions based ONLY on the graph database data.
        Reply in a concise, natural and informative manner.
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
