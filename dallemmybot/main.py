import urllib.request

import requests
from PIL import UnidentifiedImageError
from PIL import Image
from io import BytesIO
import openai
import os


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
    client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    text = ("A female chihuahua pit-bull mix with a dark brindle coat with a brindle chest "
            "and a bone in her mouth laying down in the sand on a tropical beach looking at the ocean with "
            "volumetric lighting and lens bokeh.")
    url1 = generate(client, text)
    response = requests.get(url1)
    try:
        img = urllib.request.urlopen(response.url)
        img_file = BytesIO(img.read())
        png_file = Image.open(img_file)
        png_file.save("tilly.png")
    except UnidentifiedImageError:
        print("Error: Unable to identify image format")


if __name__ == "__main__":
    main()
