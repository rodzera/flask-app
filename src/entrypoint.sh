#!/usr/bin/env bash

DB_STATUS=1

while [[ $DB_STATUS -ne 0 ]] ; do
  sleep 2
  echo "Connecting into database"
  DB_STATUS=$(python3 ./src/database_check.py)
done

echo "Database connected"
export FLASK_APP="src.app"

echo "Running migrations"
flask db upgrade --directory ./src/migrations

echo "Populating database"
flask populate_roles


if [[ -z "${HOST}" ]]; then
  export HOST="0.0.0.0"
fi

if [[ -z "${PORT}" ]]; then
  export PORT=8080
fi

echo "Server host: $HOST"
echo "Server port: $PORT"


if [[ "$DEBUG" -eq 1 || "$_DEBUG" -eq 1 || "$FLASK_DEBUG" -eq 1 ]]; then

  echo "Starting development server"
  flask --debug run -h $HOST -p $PORT

else

  if [[ -z "${WORKERS}" ]]; then
    export WORKERS=4
  fi

  if [[ -z "${THREADS}" ]]; then
    export THREADS=64
  fi

  if [[ -z "${WORKER_CONNECTIONS}" ]]; then
    export WORKER_CONNECTIONS=8192
  fi

  echo "Server workers class: gthread"
  echo "Server workers: $WORKERS"
  echo "Server threads: $THREADS"
  echo "Worker connections limit: $WORKER_CONNECTIONS"
  echo "Starting production server"
  gunicorn --bind "$HOST:$PORT" --threads $THREADS --worker-class gthread --workers $WORKERS --worker-connections $WORKER_CONNECTIONS "src.app"

fi