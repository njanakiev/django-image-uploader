#!/bin/sh

echo "Waiting for postgres ..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done

echo "PostgreSQL started"

# Run database migrations
python manage.py migrate --noinput

# Create Django super user
python manage.py createsuperuser \
  --noinput \
  --username $DJANGO_SUPERUSER_USERNAME \
  --email $DJANGO_SUPERUSER_EMAIL

# Start the Django server
exec "$@"
