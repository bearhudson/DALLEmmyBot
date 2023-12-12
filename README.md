#### A OpenAI[DALL-E] powered image bot for Lemmy


You need a .env file with the following environment variables.


```bash
OPENAI_API_KEY
MASTODON_API
LEMMY_USER
LEMMY_PASSWORD
```

Run the script wait for the list of prompts, pick the one you want, and then look for a png, jpg, and text description in an /output folder.

```bash
#!/bin/bash

echo -ne "Removing old containers if they exist.\n"

for container_id in $(docker ps -aqf "name=lemmybot"); do
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
```
