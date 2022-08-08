#!/bin/sh

python manage.py migrate
python manage.py createsuperuser --username=admin --email=admin@admin.com --noinput
python manage.py registerParsers
python manage.py collectstatic

exec "$@"