from pathlib import Path
import kuzu
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

GRAPHDB_PATH = Path(__file__).parent.parent / "graphdb"
GRAPHDB_SCHEMA_PATH = GRAPHDB_PATH / "cypher/schema.cypher"
GRAPHDB_DATABASE_PATH = GRAPHDB_PATH / "database/database.kuzu"
OLLAMA_MODEL_NAME = "llama3.2"

@tool
def query_graph_tool(cypher_query: str) -> list:
    """Retrieve GRAPH_SCHEMA database data given a single syntactically correct Cypher query.

    Args:
        cypher_query: a single syntactically correct Cypher query string to execute over GRAPH_SCHEMA database
    """
    try:
        db = kuzu.Database(GRAPHDB_DATABASE_PATH)
        conn = kuzu.Connection(db)
        cypher_query_result = conn.execute(cypher_query)
        return cypher_query_result.get_all()
    except RuntimeError as e:
        return f"""
            Failed to run given query. Review the GRAPH_SCHEMA and try again.
            Error details: {e}
        """

def main():
    """Main function to set up the graph database and process user queries."""    

    if not GRAPHDB_DATABASE_PATH.exists():
        raise SystemError("Run script `graphdb/init_graphdb.sh` script before running this example.")

    # Prepare assistant System Message
    graph_schema = GRAPHDB_SCHEMA_PATH.read_text()
    system_message = f"""
        You are an Graph Database expert with access to GRAPH_SCHEMA database.
        Your task is to generate a syntactically correct Cypher query based on the provided GRAPH_SCHEMA to answer user question.
        - STRICTLY use GRAPH_SCHEMA database data to answer user question.
        - DON'T include query details or GRAPH_SCHEMA on final response.
        - Reply in a concise and natural manner.

        <GRAPH_SCHEMA>
        {graph_schema}
        </GRAPH_SCHEMA>
    """
    
    chat_model = ChatOllama(model=OLLAMA_MODEL_NAME)
    chat_model = chat_model.bind_tools([query_graph_tool])
    agent = create_react_agent(chat_model, [query_graph_tool])
    agent = agent.with_config(recursion_limit=15)

    # Get a query from the user
    user_message = input("\nEnter your query: ")

    print("\nGenerating response...")

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]

    for step in agent.stream({"messages": messages}, stream_mode="values"):
        step["messages"][-1].pretty_print()

if __name__ == "__main__":
    main()
