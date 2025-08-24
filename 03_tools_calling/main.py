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
def run_cypher_query(cypher_query: str) -> list:
    """
    Retrieve data given a single valid Cypher query.
    Args:
        cypher_query: a single valid correct Cypher query string to execute over GRAPH_SCHEMA database
    """
    db = kuzu.Database(GRAPHDB_DATABASE_PATH)
    conn = kuzu.Connection(db)
    cypher_query_result = conn.execute(cypher_query)
    return cypher_query_result.get_all()


@tool
def get_member_names() -> list:
    """
    Retrieve all available persons names in graph data
    """
    db = kuzu.Database(GRAPHDB_DATABASE_PATH)
    conn = kuzu.Connection(db)
    cypher_query_result = conn.execute("MATCH (a:Person) RETURN a.name;")
    return cypher_query_result.get_all()


def main():
    """Main function to set up the graph database and process user queries."""    

    if not GRAPHDB_DATABASE_PATH.exists():
        raise SystemError("Run script `graphdb/init_graphdb.sh` script before running this example.")

    # Prepare assistant System Message
    graph_schema = GRAPHDB_SCHEMA_PATH.read_text()
    system_message = f"""
You are an Graph Database expert with access to GRAPH_SCHEMA database.

Always validate person name when mentioned.
Make queries to build context based ONLY on GRAPH_SCHEMA.
Generate final response ONLY based on built context.
Write the final response in a plain natural language.
Think step by step.

<GRAPH_SCHEMA>
{graph_schema}
</GRAPH_SCHEMA>
"""

    chat_model = ChatOllama(model=OLLAMA_MODEL_NAME)
    agent = create_react_agent(chat_model, [run_cypher_query, get_member_names])

    # Get a query from the user
    user_message = input("\nEnter your query: ")

    print("\nGenerating response...")

    messages = {"messages": [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]}

    for step in agent.stream(messages, stream_mode="values"):
        step["messages"][-1].pretty_print()

if __name__ == "__main__":
    main()
