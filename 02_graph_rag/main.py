import kuzu

def define_schema(conn: kuzu.Connection):
    """Define the schema"""
    print("--- Defining Schema ---")
    conn.execute("""
        CREATE NODE TABLE Person(
            name STRING,
            birth_date INT64,
            death_date INT64,
            bio STRING,
            PRIMARY KEY (name)
        )
    """)

    conn.execute("""
        CREATE NODE TABLE Occupation(
            name STRING,
            PRIMARY KEY (name)
        )
    """)

    conn.execute("""
        CREATE NODE TABLE Location(
            name STRING,
            PRIMARY KEY (name)
        )
    """)

    conn.execute("""
        CREATE NODE TABLE Hobby(
            name STRING,
            PRIMARY KEY (name)
        )
    """)

    conn.execute("CREATE REL TABLE HAS_PARENT(FROM Person TO Person)")
    conn.execute("CREATE REL TABLE IS_MARRIED_TO(FROM Person TO Person)")
    conn.execute("CREATE REL TABLE HAS_CHILDREN(FROM Person TO Person)")
    conn.execute("CREATE REL TABLE HAS_SIBLING(FROM Person TO Person)")
    conn.execute("CREATE REL TABLE HAS_OCCUPATION(FROM Person TO Occupation)")
    conn.execute("CREATE REL TABLE LIVES_IN(FROM Person TO Location)")
    conn.execute("CREATE REL TABLE HAS_HOBBY(FROM Person TO Hobby)")
    conn.execute("CREATE REL TABLE STUDIES_AT(FROM Person TO School)")

def load_data(conn: kuzu.Connection):
    """Load the data using the COPY command"""
    print("--- Loading Data from CSV ---")
    conn.execute('COPY Person FROM "./dataset/people.csv" (HEADER=true)')
    conn.execute('COPY HAS_PARENT FROM "./dataset/parents.csv" (HEADER=true)')
    conn.execute('COPY IS_MARRIED_TO FROM "./dataset/spouses.csv" (HEADER=true)')
    conn.execute('COPY HAS_CHILDREN FROM "./dataset/children.csv" (HEADER=true)')
    conn.execute('COPY HAS_OCCUPATION FROM "./dataset/occupations.csv" (HEADER=true)')
    conn.execute('COPY LIVES_IN FROM "./dataset/location.csv" (HEADER=true)')
    conn.execute('COPY HAS_HOBBY FROM "./dataset/hobbies.csv" (HEADER=true)')
    conn.execute('COPY STUDIES_AT FROM "./dataset/schools.csv" (HEADER=true)')
    print("✅ Data loaded successfully!")


def main():
    # Assume the CSV files from above exist in the same directory.
    db = kuzu.Database('./family_db_csv')
    conn = kuzu.Connection(db)

    # 3. Verify the data
    print("\n--- Verifying: Who is Homer married to? ---")
    result = conn.execute("""
        MATCH (p:Person {name: 'Homer'})-[:IS_MARRIED_TO]->(spouse:Person)
        RETURN spouse.name
    """)
    while result.has_next():
        print(result.get_next())

