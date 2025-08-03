from pathlib import Path
import kuzu
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

GRAPHDB_PATH = Path(__file__).parent.parent / "graphdb"
GRAPHDB_SCHEMA_PATH = GRAPHDB_PATH / "cypher/schema.cypher"
GRAPHDB_DATABASE_PATH = GRAPHDB_PATH / "database/database.kuzu"
OLLAMA_MODEL_NAME = "llama3.2"

def main():
    """Main function to set up the graph database and process user queries."""    

    if not GRAPHDB_DATABASE_PATH.exists():
        raise SystemError("Run script `graphdb/init_graphdb.sh` script before running this example.")
   
    graph_schema = GRAPHDB_SCHEMA_PATH.read_text()
    system_message = f"""
        You are a helpful assistant.
        Answer user questions based ONLY on the graph database data.
        Reply in a concise, natural and informative manner.
        DON'T include query details or database schema on final response.

        <GRAPH_SCHEMA>
        {graph_schema}
        </GRAPH_SCHEMA>
    """
    
    db = kuzu.Database(GRAPHDB_DATABASE_PATH)
    conn = kuzu.Connection(db)

    # Get a query from the user
    user_message = input("\nEnter your query: ")

    @tool
    def query_graph_tool(cypher_query: str) -> list:
        """Execute a Cypher query on the GRAPH_SCHEMA database and return the results.

        Args:
            cypher_query: a valid Cypher query string to execute on GRAPH_SCHEMA database
        """
        try:
            cypher_query_result = conn.execute(cypher_query)
            return cypher_query_result.get_all()
        except RuntimeError as e:
            return f"""
                Failed to run given query. Review the GRAPH_SCHEMA and try again.
                Error details: {e}
            """

    chat_model = ChatOllama(model=OLLAMA_MODEL_NAME)
    agent = create_react_agent(chat_model, [query_graph_tool])
    
    print("\nGenerating response...")

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]

    for step in agent.stream({"messages": messages}, stream_mode="values"):
        step["messages"][-1].pretty_print()

if __name__ == "__main__":
    main()
