#!/bin/bash

docker build -f dockerfile.backend -t sensors-be .
docker run --name sensors-be senors-be
