import requests
from urllib import parse
import spacy


def get_topic():
    r_topic = requests.get('https://en.wikipedia.org/wiki/Special:Random')
    decoded_url = parse.unquote(r_topic.url)
    topic_index = decoded_url.rfind('/')
    topic_string = decoded_url[topic_index + 1:].replace('_', ' ')
    return topic_string, decoded_url


def get_verified_topic():
    verified = False
    nlp = spacy.load("en_core_web_sm")
    # TODO: Add more language support
    topic = None
    url = None
    while not verified:
        topic, url = get_topic()
        str_check = nlp(topic)
        if len(str_check.ents) > 0:
            for entry in str_check.ents:
                print(entry.text, entry.label_)
                if (entry.label_ == "PERSON" or
                        entry.label_ == "EVENT" or
                        entry.label_ == "ORG"):
                    topic, url = get_topic()
                verified = True
    return topic, url
