from pythorhead import Lemmy
import os
from community_list import community_list

USER = os.getenv("LEMMY_USER")
PASSWORD = os.getenv("LEMMY_PASSWORD")

lemmy_obj = Lemmy(api_base_url="https://lemm.ee")
lemmy_obj.log_in(USER, PASSWORD)


def create_lemmy_post(name, url, body):
    try:
        community_id = lemmy_obj.discover_community(community_list[0])
        lemmy_obj.post.create(community_id, name=name, url=url, body=body)
    except Exception:
        print("Error posting to Lemmy")
