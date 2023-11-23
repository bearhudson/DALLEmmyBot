import urllib.request
import urllib.parse
from random import choice
import requests
from PIL import UnidentifiedImageError
from PIL import Image
from io import BytesIO
import openai
import os
from griptape.structures import Agent
import time
from shot_type import shot_type_list, lens_type


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
        full_text = gt_agent.run(f"Write me a brief paragraph description about {r_topic_str} "
                                 f"with a {choice(shot_type_list)}, and {choice(lens_type)} style lens, "
                                 f"describe the scene and relative, local art style from the perspective of a painter "
                                 f"painting a movie scene at a specific, random time in the day and include as much "
                                 f"detail as possible about the colors, describe the subjects and objects in the scene "
                                 f"but do not use the word camera and keep the view static and obey the rule of thirds "
                                 f"including taking into consideration the following details -- {item_description.value}.")
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


if __name__ == "__main__":
    main()
