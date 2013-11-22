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
    "You become a goat of the goat tower.",
    "You die an old man at the top of the tower, your goat herd surrounding your bed.",
    "You successfully communicate with the goat imperialist. You are financially drained after being mentally frozen by his academic wisdom.",
    "The goat laughs \"BAAAHHHHHHHHHHAHAHA\" as you are forced to leap from the goat tower",
    "The scroll from the elder goat states there is a passage way with a green star engraved. You might become rich if you can find this passage.",
    "The poster reads: \"There is no futBAAAAAAHHHHure but what we mBAAAAHHHHHHHHke for ouBAAAAAAHHHHHHHHHHHHHrselves.\"",
]

def run(data, settings):
    if data['payload'] == 'goat tower':
        say = '{nick}: {outcome}'.format(nick=data['nick'],
                                         outcome=random.choice(goat_stuff))
        return say
