#!/bin/bash

# if the script cannot be found, change the file from CRLF to LF

# create .env file from environment variables, for python settings
echo "Creating .env file from environment variables..."

cat > .env <<EOF
# secret key for website
SECRET_KEY=$SECRET_KEY
# database setting
DATABASE=$DATABASE
POSTGRE_USERNAME=$POSTGRE_USERNAME
POSTGRE_PASSWORD=$POSTGRE_PASSWORD
POSTGRE_HOST=$POSTGRE_HOST
POSTGRE_PORT=$POSTGRE_PORT
# initial user setting
DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME
DJANGO_SUPERUSER_EMAIL=$DJANGO_SUPERUSER_EMAIL  
DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD
# allow hosts for website
ALLOWED_HOSTS=$ALLOWED_HOSTS
# log file config, the log file name should be in (relative path)
DJANGO_LOG_FILE_NAME=$DJANGO_LOG_FILE_NAME
DJANGO_LOG_LEVEL=$DJANGO_LOG_LEVEL

# debug parameter (onetime)
DEBUG=$DEBUG

# nginx settings
NGINX_PORT=$NGINX_PORT
DJANGO_PORT=$DJANGO_PORT

# media and static root for production (absolute path), also need to be configured in nginx settings
PRODUCTION_MEDIA_ROOT=$PRODUCTION_MEDIA_ROOT
PRODUCTION_STATIC_ROOT=$PRODUCTION_STATIC_ROOT
EOF

echo ".env file created successfully."

# rewrite nginx settings

# laod env variables: https://stackoverflow.com/questions/19331497/set-environment-variables-from-file-of-key-value-pairs#comment37343914_20909045
export $(grep -v '^#' .env | xargs)

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    echo "http://" $POSTGRE_HOST ":" $POSTGRE_PORT

    while ! nc -z $POSTGRE_HOST $POSTGRE_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations
python manage.py migrate

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    echo "Trying to create user based on environment variables, error message after first creation is normal."
    python manage.py createsuperuser \
        --noinput 
fi

exec "$@"