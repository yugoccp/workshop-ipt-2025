docker run --rm -p 8000:8000 \
    -v ./database:/database \
    -e KUZU_FILE="database.kuzu" \
    kuzudb/explorer:latest