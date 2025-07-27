import os
import kuzu
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

DATABASE_PATH = './database/database.kuzu'
OLLAMA_MODEL_NAME = "llama3.2"  # Ollama model for chat
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
GRAPH_DATA_LOAD = """
    COPY Person FROM "./dataset/people.csv";
    COPY Occupation FROM "./dataset/occupations.csv";
    COPY Location FROM "./dataset/locations.csv";
    COPY Hobby FROM "./dataset/hobbies.csv";
    COPY School FROM "./dataset/schools.csv";
    COPY HAS_PARENT FROM "./dataset/has_parents.csv";
    COPY HAS_CHILDREN FROM "./dataset/has_children.csv";
    COPY HAS_SIBLING FROM "./dataset/has_siblings.csv";
    COPY HAS_OCCUPATION FROM "./dataset/has_occupations.csv";
    COPY HAS_HOBBY FROM "./dataset/has_hobby.csv";
    COPY LIVES_IN FROM "./dataset/lives_in.csv";
    COPY IS_MARRIED_TO FROM "./dataset/married_to.csv";
    COPY STUDIES_AT FROM "./dataset/studies_at.csv";
"""

def main():
    """Main function to set up the graph database and process user queries."""


    is_new_database = not os.path.exists(DATABASE_PATH)
    db = kuzu.Database(DATABASE_PATH)
    conn = kuzu.Connection(db)

    if is_new_database:
        print("\nFirst time setting up Kuzu database...")
        print("\nDefining Graph schema...")
        conn.execute(GRAPH_SCHEMA)
        
        print("\nLoading Data from CSV...")
        conn.execute(GRAPH_DATA_LOAD)

     # Get a query from the user
    query = input("\nEnter your query: ")

    # Generate a response using the chat model
    prompt_cypher = f"""
        Generate cypher query based on graph database schema to support answer the user question.
        Return the query as a JSON object with the key "cypher".

        <GRAPH_SCHEMA>
        {GRAPH_SCHEMA}
        </GRAPH_SCHEMA>

        <USER_QUESTION>
        {query}
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
        Based on the cypher query and it's result, answer the user's question:
        
        <QUERY_RESULTS>
        Query: {cypher_query}
        Result: {cypher_results}
        </QUERY_RESULTS>

        <USER_QUESTION>
        {query}
        </USER_QUESTION>
        """
    
    print("\nGenerating response...")
    response = chat_model.invoke(prompt_question)

    print("\nResponse:", response.content)

if __name__ == "__main__":
    main()
