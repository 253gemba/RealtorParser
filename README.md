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
    docker-compose build
    docker-compose up -d
    ```
