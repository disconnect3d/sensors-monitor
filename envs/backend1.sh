#!/bin/bash
echo "[*] Setting envvars for backend1"
export DJANGO_USE_X_FORWARDED_HOST=True
export DJANGO_APP_DB_PATH=/db/backend1.sqlite3
echo "[*] Envvars for backend1 set"
