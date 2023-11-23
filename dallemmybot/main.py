import urllib.request
import urllib.parse
from random import choice
import requests
from PIL import UnidentifiedImageError
from PIL import Image
from io import BytesIO
import openai
import os
import json
from griptape.structures import Agent
import time
from shot_type import shot_type_list, lens_type
from community_list import community_list
from lemmy import login, get_community


def generate(client, text):
    res = client.images.generate(
        model="dall-e-3",
        quality="hd",
        prompt=text,
        n=1,
        size="1792x1024",
    )
    image_url = res.data[0]
    print(image_url.url)
    return image_url.url


def main():
    try:
        t_stamp = int(time.time())
        client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        gt_agent = Agent()
        r_topic = requests.get('https://en.wikipedia.org/wiki/Special:Random')
        decoded_url = urllib.parse.unquote(r_topic.url)
        topic_index = decoded_url.rfind('/')
        r_topic_str = decoded_url[topic_index + 1:].replace('_', ' ')
        item_description_full = gt_agent.run(f"Tell me some brief details about {r_topic_str}.")
        item_description = item_description_full.output_task.output
        full_text = gt_agent.run(f"Describe for me a painting about {r_topic_str} "
                                 f"with a {choice(shot_type_list)}, and {choice(lens_type)} style lens, "
                                 f"with the following details: {item_description.value} -- using a relative "
                                 f"art style for the area and time.")
        url1 = generate(client, str(full_text.output_task))
        response = requests.get(url1)
    except openai.BadRequestError:
        print("Error generating prompt")
        exit(1)
    try:
        text_file = f"./output/{t_stamp}-{r_topic_str}.txt"
        image_file = f"./output/{t_stamp}-{r_topic_str}.png"
        img = urllib.request.urlopen(response.url)
        img_file = BytesIO(img.read())
        png_file = Image.open(img_file)
        png_file.save(image_file)
        with open(text_file, 'w') as file:
            file.write(f"{item_description.value}\n\n{str(full_text.output_task)}")
    except UnidentifiedImageError:
        print("Error: Unable to identify image format")
        exit(1)
    login()
    community_id_list = []
    community_json = {}
    for community in community_list:
        cur_community = get_community(community)
        community_json = json.loads(cur_community)
    community_id_list.append(community_json["community_view"]["community"]["id"])
    for comm_id in community_id_list:
        print(comm_id)


if __name__ == "__main__":
    main()
