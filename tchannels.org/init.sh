#!/bin/bash

docker network create tchan_net

docker run -d \
  --name tchannels_db \
  --network tchan_net \
  --restart unless-stopped \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=tchannels \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16

docker build -t tchannels_image -f ./app/dockerfile ./app/

docker run -d \
    --network tchan_net \
    -p 127.0.0.1:10118:80 \
    --restart unless-stopped \
    --name tchannels_app \
    tchannels_image
