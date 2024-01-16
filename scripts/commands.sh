#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

echo "ℹ️ Starting the script"

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..." &
  sleep 0.1
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

echo "ℹ️ Running 'collectstatic'..."
python manage.py collectstatic --noinput

echo "ℹ️ Running 'makemigrations'..."
python manage.py makemigrations --noinput

echo "ℹ️ Running 'migrate'..."
python manage.py migrate --noinput

echo "ℹ️ Running 'runserver'..."
python manage.py runserver 0.0.0.0:8000
