#!/bin/bash

set -e

. /envs.sh

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
./manage.py runserver 0.0.0.0:8000

# ON PRODUCTION LAUNCH AS:
# DJANGO_SETTINGS_MODULE=sensors.prod_settings gunicorn --workers 2 --bind 0.0.0.0:8000 --access-logfile - sensors.wsgi:application
