import os
import json
from mastodon import Mastodon
from mastodon import MastodonError

# Create an instance of the Mastodon class
API_KEY = os.getenv("MASTODON_API")
INSTANCE = "https://mastodon.world"


def make_post(image, description, title):
    mastodon = Mastodon(
        access_token=API_KEY,
        api_base_url=INSTANCE
    )
    try:
        media = mastodon.media_post(image, description=title)
        post = mastodon.status_post(description, media_ids=media)
        return post["uri"]
    except MastodonError:
        print("Mastodon Error.")
