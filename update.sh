#!/bin/bash

set -e

CONTAINER_NAME="cities-bot"
IMAGE_NAME="quixx21/cities-bot:latest"

docker rm -f $CONTAINER_NAME || true
docker rmi $IMAGE_NAME || true
docker pull $IMAGE_NAME
docker run -d --name $CONTAINER_NAME \
  -e BOT_TOKEN=8419311587:AAGwiLRgsaC1vuWj-SbhnjmWZmjjscE_r-U\
  $IMAGE_NAME
docker start $CONTAINER_NAME
echo "Cities-Bot started. Check your bot"
