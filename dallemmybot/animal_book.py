import requests
from bs4 import BeautifulSoup
import random


def get_animal_name():
    animal_name = ""
    url = "https://en.wikipedia.org/wiki/List_of_animal_names"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the table with class "wikitable sortable jquery-tablesorter"
        animal_tables = soup.find_all('table', class_="wikitable")
        for table in animal_tables:
            animal_names = [row.text.strip() for row in table.find_all('td', class_='navbox-list')]
            for animal in animal_names:
                print(animal)
        return animal_name
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []


if __name__ == "__main__":
    random_animal = get_animal_name()
    if random_animal:
        print("Random Animal:", random_animal)
