import random
from animal_lists import animal_species
from animal_lists import gen_animal_terms

animal = random.choice(animal_species)
mutation = random.choice(gen_animal_terms)

print(f"Write two sentences about a {animal} with a mutation from the {mutation} taxonomy.")

