#!/bin/bash

docker rmi -f sensors-be
docker rm -f sensors-be

docker build -f dockerfile.backend -t sensors-be .
docker run -d --name sensors-be -v $HOME/sensors_deploy/envvars.sh:/envvars.sh -v $HOME/sensors_deploy/db:/db -p 1337:8000 -p 31337:8005 sensors-be
