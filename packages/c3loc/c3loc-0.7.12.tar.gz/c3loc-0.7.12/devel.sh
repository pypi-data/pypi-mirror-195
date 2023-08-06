#!/bin/sh

user="c3loc"
db="c3loc-test"

container_id=$(docker run -it --rm -p5432:5432 -d \
    -ePOSTGRES_HOST_AUTH_METHOD=trust -ePOSTGRES_DB="$db" \
    -ePOSTGRES_USER="$user" postgres:12-alpine)

echo "Postgresql running under Docker: $container_id"
sleep 1
alembic upgrade head
DB_USER="$user" DB_HOST=127.0.0.1 DB_NAME="$db" c3loc_ingest -p 9999 &
DB_USER="$user" DB_HOST=127.0.0.1 DB_NAME="$db" c3loc_api -p 10999 
docker kill "$container_id"
