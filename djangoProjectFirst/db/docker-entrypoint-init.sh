#!/bin/bash

# Wait for PostgreSQL to be ready on localhost:5432
echo "Waiting for PostgreSQL to start..."
until pg_isready -h db -p 5432 -U postgres; do
    echo "PostgreSQL is not ready yet, sleeping for 1 second..."
    sleep 1
done
echo "PostgreSQL is ready."

# Check if pharmdb exists
if ! psql -h db -p 5432 -U postgres -lqt | cut -d \| -f 1 | grep -qw pharmdb; then
    echo "Creating pharmdb database..."
    if ! psql -h db -p 5432 -U postgres -c "CREATE DATABASE pharmdb;"; then
        echo "Error: Failed to create pharmdb database."
        exit 1
    fi
    echo "pharmdb created."
else
    echo "pharmdb already exists."
fi

# Run the original PostgreSQL entrypoint
exec docker-entrypoint.sh "$@"