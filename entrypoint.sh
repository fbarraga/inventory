#!/bin/sh
set -e

# Amb PostgreSQL, esperar que la BD accepti connexions (per defecte s'usa SQLite)
if [ "$DB_ENGINE" = "django.db.backends.postgresql" ]; then
  echo "Esperant la base de dades..."
  i=0
  until python -c "import os, psycopg2; psycopg2.connect(host=os.environ['DB_HOST'], dbname=os.environ['DB_NAME'], user=os.environ['DB_USER'], password=os.environ['DB_PASSWORD'], port=os.environ.get('DB_PORT', '5432'), connect_timeout=2).close()" 2>/dev/null; do
    i=$((i + 1))
    if [ "$i" -ge 30 ]; then
      echo "La base de dades no respon després de 30 intents"
      exit 1
    fi
    sleep 1
  done
fi

echo "Aplicant migracions..."
python manage.py migrate --noinput

echo "Comprovant la configuració de producció..."
python manage.py check --deploy --fail-level ERROR

exec "$@"
