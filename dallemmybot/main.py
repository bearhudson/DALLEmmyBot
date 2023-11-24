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
from lemmy_funct import lemmy_post
from mastodon_funct import make_post as mastodon_post


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
        item_description_full = gt_agent.run(f"Tell me some brief details about {r_topic_str} "
                                             f"using 400 words or less.")
        item_description = item_description_full.output_task.output
        full_text = gt_agent.run(f"Describe for me a painting about {r_topic_str} "
                                 f"with a {choice(shot_type_list)}, and {choice(lens_type)} style lens, "
                                 f"with the following details: {item_description.value} -- using a relative "
                                 f"art style for the location and timeframe.")
        url1 = generate(client, str(full_text.output_task))
        response = requests.get(url1)
    except openai.BadRequestError:
        print("Error generating prompt")
        exit(1)
    try:
        text_file = f"./output/{t_stamp}-{r_topic_str}.txt"
        image_file = f"./output/{t_stamp}-{r_topic_str}.png"
        jpeg_file = f"./output/{t_stamp}-{r_topic_str}.jpeg"
        img = urllib.request.urlopen(response.url)
        img_file = BytesIO(img.read())
        png_file = Image.open(img_file)
        png_file.save(image_file)
        png_file.convert("RGB").save(jpeg_file, "JPEG", quality=99)
        with open(text_file, 'w') as file:
            file.write(f"{item_description.value}\n\n{str(full_text.output_task)}")
    except UnidentifiedImageError:
        print("Error generating images.")
        exit(1)
    truncate_out = str(item_description.value).split('\n')[0]
    print(truncate_out)
    url = mastodon_post(
        image=image_file,
        title=f"{truncate_out}",
        description=f"{truncate_out}\n\n{decoded_url}\n\n#DALLE #DALLE3 #AIart #openai #llm #imagegeneration #wiki "
                    f"#wikipedia")
    lemmy_post(url=url,
               title=f"{r_topic_str}",
               description=f"{truncate_out}")


if __name__ == "__main__":
    main()
