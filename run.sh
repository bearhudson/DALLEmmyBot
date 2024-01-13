#!/bin/bash

echo -ne "Removing old containers if they exist.\n"

for container_id in $(docker ps -aqf "name=dallemmybot"); do
    echo "Stopping and removing container with ID: $container_id"
    docker stop "$container_id"
    docker rm "$container_id"
done
  
echo -ne "Starting build.\n"
docker build -t dallemmybot .

echo -ne "Running Container.\n"
docker run --name dallemmybot --env-file .env -it dallemmybot 

echo -ne "Copying files out of container.\n"
docker cp dallemmybot:/usr/src/app/output .

for container_id in $(docker ps -aqf "name=dallemmybot"); do
    echo "Stopping and removing container with ID: $container_id"
    docker stop "$container_id"
    docker rm "$container_id"
done