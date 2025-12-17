#!/bin/bash
set -e

# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
./scripts/wait_for_it.sh ${POSTGRES_HOST:-postgres}:${POSTGRES_PORT:-5432} -t 60

# Wait for Redis
echo "Waiting for Redis..."
./scripts/wait_for_it.sh redis:6379 -t 30

# Wait for Neo4j
echo "Waiting for Neo4j..."
./scripts/wait_for_it.sh neo4j:7687 -t 60

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files (production only)
if [ "$DJANGO_ENV" = "production" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
fi

# Execute the main command
exec "$@"

