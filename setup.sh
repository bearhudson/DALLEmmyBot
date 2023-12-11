#!/bin/bash

docker build -t dallemmybot .
docker run --env-file .env -it dallemmybot 
docker cp dallemmybot:/usr/src/app/dallemmybot/output .
