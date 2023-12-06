FROM python:3.10
RUN python -m spacy download xx_ent_wiki_sm; \
    python -m spacy download en_core_web_lg

