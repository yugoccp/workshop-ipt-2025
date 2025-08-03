kuzu ./database/database.kuzu < ./cypher/schema.cypher
kuzu ./database/database.kuzu < ./cypher/data.cypher
docker run --rm -p 8000:8000 \
    -v ./database:/database \
    -e KUZU_FILE="database.kuzu" \
    kuzudb/explorer:latest