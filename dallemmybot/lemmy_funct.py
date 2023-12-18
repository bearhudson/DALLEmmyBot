from pythorhead import Lemmy
import os
from community_list import community_list

USER = os.getenv("LEMMY_USER")
PASSWORD = os.getenv("LEMMY_PASSWORD")


def create_lemmy_posts(name, url, body):
    for instance, community in community_list.items():
        print(instance)
        print(community)
        lemmy_obj = Lemmy(api_base_url=instance)
        lemmy_obj.log_in(USER, PASSWORD)
        try:
            community_id = lemmy_obj.discover_community(community)
            lemmy_obj.post.create(community_id, name=name, url=url, body=body)
        except Exception:
            print("Error posting to Lemmy")
