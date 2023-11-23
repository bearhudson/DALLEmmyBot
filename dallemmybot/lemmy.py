import requests
import json
import os

USER = os.getenv("LEMMY_USER")
PASSWORD = os.getenv("LEMMY_PASSWORD")

bearer_token = ""


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


def get_community(comm_str):
    url = f"https://lemm.ee/api/v3/community?name={comm_str}"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {bearer_token}"
    }
    response = requests.get(url, headers=headers)
    print(response.text)
    return response.text
