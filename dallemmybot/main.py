import io
import urllib.request

import requests
from PIL import UnidentifiedImageError
from PIL import Image
from io import BytesIO
import openai
import os


def generate(client, text):
    res = client.images.generate(
        prompt=text,
        n=1,
        size="1024x1024",
    )
    print(res.data[0])
    image_url = res.data[0]
    print(image_url.url)
    return image_url.url


def main():
    client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    text = "A large female chihuahua mix with a full, dark, brindle coat and a bone in her mouth on a tropical beach."
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
