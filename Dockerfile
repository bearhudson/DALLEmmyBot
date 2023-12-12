FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the dependencies file to the working directory
COPY pyproject.toml poetry.lock* ./

# Install any dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi \
    && python -m spacy download xx_ent_wiki_sm \
    && python -m spacy download en_core_web_lg \
    && mkdir output
# Copy the content of the local src directory to the working directory
COPY . ./

# Specify the command to run on container start
CMD [ "python", "dallemmybot/dallemmybot.py" ]
