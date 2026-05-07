#!/bin/bash
docker build --no-cache -t tchannels_image -f ./app/dockerfile ./app/
docker stop tchannels_app || true
docker rm tchannels_app || true
docker run -d \
    -p 127.0.0.1:8501:80 \
    --network tchan_net \
    --restart unless-stopped \
    --name tchannels_app \
    tchannels_image
