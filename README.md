# Realtor's parser backend

## How to run

1. Create __.env__ file with the following variables:
    ```
    POSTGRES_NAME=''
    POSTGRES_USER=''
    POSTGRES_PASSWORD='!'

    DJANGO_SUPERUSER_PASSWORD=''
    DJANGO_SECRET_KEY=''
    ```
2. Run
    ```
    docker-compose up -d --build
    docker-compose exec app python manage.py migrate
    docker-compose exec app python manage.py createsuperuser --username=admin --email=admin@admin.com --noinput
    docker-compose exec app python manage.py registerParsers
    docker-compose exec app python manage.py collectstatic
    ```
