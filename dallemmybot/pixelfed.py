import os
from mastodon import Mastodon
from mastodon import MastodonAPIError

# Create an instance of the Mastodon class
API_KEY = os.getenv("MASTODON_API")
INSTANCE = "https://mastodon.world"

mastodon = Mastodon(
    access_token=API_KEY,
    api_base_url=INSTANCE
)
# Post a new status update
try:
    mast_post = mastodon.status_post("Hello, Mastodon!")
    print(mast_post)
except MastodonAPIError:
    print("API Error. Exiting.")
    exit(1)
