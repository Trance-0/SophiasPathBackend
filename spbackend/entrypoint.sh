#!/bin/bash
# if the script cannot be found, change the file from CRLF to LF

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py makemigrations
python manage.py migrate

if [ "$DJANGO_SUPERUSER_USERNAME" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

# Update the password for the superuser if required
if [ -n "$DJANGO_SUPERUSER_PASSWORD" ]
then
  echo "[INFO] Setting Django superuser password"
  $DJANGO_ADMIN shell -c "
  from django.contrib.auth import get_user_model

  user = get_user_model().objects.get(username='$DJANGO_SUPERUSER_USERNAME')
  user.set_password('$DJANGO_SUPERUSER_PASSWORD')
  user.save()"
fi

exec "$@"