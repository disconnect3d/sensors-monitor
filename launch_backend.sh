#!/bin/bash

set -e
export DJANGO_SETTINGS_MODULE=sensors.deploy_settings

./manage.py collectstatic --noinput

call_loaddata=false

if [ ! -f ${DJANGO_APP_DB_PATH} ]; then
    echo "[*] Database file doesn't exist in ${DJANGO_APP_DB_PATH}. Gonna loaddata after migrate."
    call_loaddata=true
fi
./manage.py migrate

if [ "$call_loaddata" = true ]; then
    ./manage.py loaddata 002fixture.json
fi

echo "[*] Running runserver"
gunicorn --workers 2 --bind 0.0.0.0:8000 --access-logfile - sensors.wsgi:application
#./manage.py runserver 0.0.0.0:8000