import random

goat_stuff = [
    "You die trying to reach the goat tower.",
    "You die trying to take your first step into the goat tower.",
    "You die after trying to fight with a goat from the goat tower.",
    "You die falling from the goat tower.",
    "You die by a misstep scaling the goat tower.",
    "You die by the horns of a goat halfway up the goat tower.",
    "You successfully enter the goat tower.",
    "You talk to the goat master of the goat tower. He imparts upon you great and dark goat wisdom.",
    "You learn the secrets of the goat tower.",
    "You become a goat of the goat tower."
]

def run(data, settings):
    if data['payload'] == 'goat tower':
        return random.choice(goat_stuff)
