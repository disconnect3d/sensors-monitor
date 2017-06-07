#!/bin/bash
echo "[*] Setting envvars for backend2"
export DJANGO_USE_X_FORWARDED_HOST=True
export DJANGO_APP_DB_PATH=/db/backend2.sqlite3
echo "[*] Envvars for backend2 set"