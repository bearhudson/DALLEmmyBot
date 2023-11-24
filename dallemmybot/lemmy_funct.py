import requests
from requests import RequestException
import json
import os
from community_list import community_list

USER = os.getenv("LEMMY_USER")
PASSWORD = os.getenv("LEMMY_PASSWORD")


def login():
    url = "https://lemm.ee/api/v3/user/login"
    payload = {
        "username_or_email": f"{USER}",
        "password": f"{PASSWORD}"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)
    jwt = json.loads(response.text)
    bearer_token = jwt["jwt"]
    return bearer_token


def get_community(bearer_token, comm_str):
    try:
        url = f"https://lemm.ee/api/v3/community?name={comm_str}"
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {bearer_token}"
        }
        response = requests.get(url, headers=headers)
        community_json = json.loads(response.text)
        return community_json["community_view"]["community"]["id"]
    except RequestException:
        print("Error getting communities.")
        return False


def make_post(bearer_token, community_id, title, url, description):
    try:
        api_url = "https://lemm.ee/api/v3/post"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {bearer_token}"
        }
        payload = {
            "auth": {
                "username_or_email": f"{USER}",
                "password": f"{PASSWORD}",
            },
            "name": f"{title}",
            "community_id": int(community_id),
            "url": f"{url}",
            "body": f"{description}"
        }
        print(f"Making lemmy post in {community_id} {url} -- {title} -- {description}")
        response = requests.post(api_url, headers=headers, json=payload)
        print(f"Lemmy post: {response}")
        return True
    except RequestException:
        return False


def lemmy_post(url, title, description):
    bearer_token = login()
    for community in community_list:
        comm_id = get_community(bearer_token=bearer_token, comm_str=community)
        print(comm_id)
        make_post(bearer_token=bearer_token,
                  community_id=comm_id,
                  url=url,
                  title=title,
                  description=description)
