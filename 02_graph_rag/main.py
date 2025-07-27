import os
import kuzu
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

OLLAMA_MODEL_NAME = "gemma3"  # Ollama model for chat
GRAPH_SCHEMA = """
    CREATE NODE TABLE Person(name STRING, birth_date DATE, death_date DATE, bio STRING, PRIMARY KEY (name));
    CREATE NODE TABLE Occupation(name STRING, PRIMARY KEY (name));
    CREATE NODE TABLE Location(name STRING, PRIMARY KEY (name));
    CREATE NODE TABLE Hobby(name STRING, PRIMARY KEY (name));
    CREATE NODE TABLE School(name STRING, PRIMARY KEY (name));
    CREATE REL TABLE HAS_PARENT(FROM Person TO Person);
    CREATE REL TABLE HAS_CHILDREN(FROM Person TO Person);
    CREATE REL TABLE HAS_SIBLING(FROM Person TO Person);
    CREATE REL TABLE HAS_OCCUPATION(FROM Person TO Occupation);
    CREATE REL TABLE HAS_HOBBY(FROM Person TO Hobby);
    CREATE REL TABLE IS_MARRIED_TO(FROM Person TO Person);
    CREATE REL TABLE LIVES_IN(FROM Person TO Location);
    CREATE REL TABLE STUDIES_AT(FROM Person TO School);
    """
def get_chat_model() -> ChatOllama:
    """Initialize the Ollama chat model."""
    return ChatOllama(model=OLLAMA_MODEL_NAME)

def define_schema(conn: kuzu.Connection):
    """Define the schema"""
    conn.execute(GRAPH_SCHEMA)

def load_data(conn: kuzu.Connection):
    """Load the data using the COPY command"""
    conn.execute('COPY Person FROM "./dataset/people.csv"')
    conn.execute('COPY Occupation FROM "./dataset/occupations.csv"')
    conn.execute('COPY Location FROM "./dataset/locations.csv"')
    conn.execute('COPY Hobby FROM "./dataset/hobbies.csv"')
    conn.execute('COPY School FROM "./dataset/schools.csv"')
    conn.execute('COPY HAS_PARENT FROM "./dataset/has_parents.csv"')
    conn.execute('COPY HAS_CHILDREN FROM "./dataset/has_children.csv"')
    conn.execute('COPY HAS_OCCUPATION FROM "./dataset/has_occupations.csv"')
    conn.execute('COPY HAS_HOBBY FROM "./dataset/has_hobby.csv"')
    conn.execute('COPY LIVES_IN FROM "./dataset/lives_in.csv"')
    conn.execute('COPY IS_MARRIED_TO FROM "./dataset/married_to.csv"')
    conn.execute('COPY STUDIES_AT FROM "./dataset/studies_at.csv"')
    
def main():
    """Main function to set up the graph database and process user queries."""

    database_path = './database/database.kuzu'
    is_new_database = not os.path.exists(database_path)

    db = kuzu.Database(database_path)
    conn = kuzu.Connection(db)

    if is_new_database:
        print("\nDefining Graph schema...")
        define_schema(conn)
        
        print("\nLoading Data from CSV...")
        load_data(conn)

     # Get a query from the user
    query = input("\nEnter your query: ")

    # Generate a response using the chat model
    cypher_prompt = f"""
        Generate cypher query based on graph database schema to support answer the user question.
        Return the query as a JSON object with the key "cypher".

        <DB_SCHEMA>
        {GRAPH_SCHEMA}
        </DB_SCHEMA>

        <USER_QUESTION>
        {query}
        </USER_QUESTION>
        """
    
    print("\nGenerating Cypher Query...")
    chat_model = get_chat_model()
    response = chat_model.invoke(cypher_prompt)

    print(response.content)

    print("\nExecuting Cypher Query...")
    json_parser = JsonOutputParser()
    json_response = json_parser.parse(text=response.content)
    cypher_query = json_response["cypher"]
    result = conn.execute(cypher_query)
    cypher_results = result.get_all()

    for row in cypher_results:
        print(row)
        print(10 * "-")
    
    question_prompt = f"""
        You are a helpful assistant.

        Based on the cypher query and it's result, answer the user's question:
        
        <QUERY_RESULTS>
        {cypher_results}
        </QUERY_RESULTS>

        <USER_QUESTION>
        {query}
        </USER_QUESTION>
        """
    
    print("\nGenerating response...")
    chat_model = get_chat_model()
    response = chat_model.invoke(question_prompt)

    print("\nResponse:", response.content)

if __name__ == "__main__":
    main()