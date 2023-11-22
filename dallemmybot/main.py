import urllib.request
import urllib.parse
import requests
from PIL import UnidentifiedImageError
from PIL import Image
from io import BytesIO
import openai
import os
from griptape.structures import Agent
import time


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
    t_stamp = int(time.time())
    client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    gt_agent = Agent()
    r_topic = requests.get('https://en.wikipedia.org/wiki/Special:Random')
    decoded_url = urllib.parse.unquote(r_topic.url)
    topic_index = decoded_url.rfind('/')
    r_topic_str = decoded_url[topic_index + 1:].replace('_', ' ')
    item_description = gt_agent.run(f"Tell me some brief details about {r_topic_str}.")
    full_text = gt_agent.run(f"Write me a sentence about {r_topic_str} from the perspective of a director writing a "
                             f"movie scene at a random time in the day and include as much detail as possible "
                             f"about the colors, angles, subjects and objects in the scene but do not use "
                             f"the word camera and keep the view static and obey the rule of thirds including the "
                             f"following details -- {item_description}.")
    print(full_text.output_task)
    url1 = generate(client, str(full_text.output_task))
    response = requests.get(url1)
    try:
        text_file = f"{t_stamp}-{r_topic_str}.txt"
        image_file = f"{t_stamp}-{r_topic_str}.png"
        img = urllib.request.urlopen(response.url)
        img_file = BytesIO(img.read())
        png_file = Image.open(img_file)
        png_file.save(image_file)
        with open(text_file, 'w') as file:
            file.write(str(full_text.output_task))
    except UnidentifiedImageError:
        print("Error: Unable to identify image format")


if __name__ == "__main__":
    main()
