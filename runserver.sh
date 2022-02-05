#!/bin/sh

echo "Collectstatic"
python manage.py collectstatic --noinput
echo "compilemessages"
python manage.py compilemessages -l fr
echo "migrate"
python manage.py migrate
echo "Gunicorn"
gunicorn village_des_benjamins.wsgi --bind=0.0.0.0:80
