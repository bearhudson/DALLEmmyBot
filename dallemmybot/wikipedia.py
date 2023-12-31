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
    nlp_en = spacy.load("en_core_web_lg")
    nlp_wiki = spacy.load("xx_ent_wiki_sm")
    # TODO: Add more language support
    topic = None
    url = None
    while not verified:
        topic, url = get_topic()
        str_check = nlp_en(topic)
        if len(str_check.ents) > 0:
            for entry in str_check.ents:
                if (entry.label_ == "PERSON" or
                        entry.label_ == "PER" or
                        entry.label_ == "EVENT" or
                        entry.label_ == "ORG" or
                        entry.label_ == "GPE"):
                    topic, url = get_topic()
        str_check = nlp_wiki(topic)
        if len(str_check.ents) > 0:
            for entry in str_check.ents:
                if (entry.label_ == "PERSON" or
                        entry.label_ == "PER" or
                        entry.label_ == "EVENT" or
                        entry.label_ == "ORG" or
                        entry.label_ == "GPE"):
                    topic, url = get_topic()
                verified = True
    return topic, url


def get_verified_topic_list(topic_num):
    result_list = []
    for _ in range(topic_num):
        result = get_verified_topic()  # Assuming get_verified_topic is a function
        result_list.append(result)
    return result_list


def wiki_return_topic(topic_count):
    print("Fetching topics...")
    topic_list = get_verified_topic_list(topic_count)
    for title, url in enumerate(topic_list, start=1):
        print(f"{title}. {url}")
    while True:
        try:
            user_choice = int(input(f"Select an item (1-{topic_count}): "))
            if 1 <= user_choice <= topic_count:
                selected_item = topic_list[user_choice - 1]
                return selected_item
            else:
                print(f"Invalid choice. Please enter a number between 1 and {topic_count}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
