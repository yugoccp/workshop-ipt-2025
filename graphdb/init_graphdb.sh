echo "Building database Schema..."
kuzu ./database/database.kuzu < ./cypher/schema.cypher

echo "Loading CSV data to Graph..."
kuzu ./database/database.kuzu < ./cypher/data.cypher

CONTAINER_NAME="kuzudb_explorer"

if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Stopping existing kuzudb/explorer container..."
    docker stop "${CONTAINER_NAME}"
fi

echo "Starting kuzudb/explorer container..."
docker run --rm -d --name "${CONTAINER_NAME}" -p 8000:8000 \
    -v ./database:/database \
    -e KUZU_FILE="database.kuzu" \
    kuzudb/explorer:latest