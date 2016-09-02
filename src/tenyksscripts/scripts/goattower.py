import random

goat_stuff = [
    "Fuck you.",
    "You die trying to reach the goat tower.",
    "You die trying to take your first step into the goat tower.",
    "You die after trying to fight with a goat from the goat tower.",
    "You die falling from the goat tower.",
    "You manage to heave 2 goats for 9M. Fucking awful.",
    "You die by a misstep scaling the goat tower.",
    "You die. No reason, just death.",
    "You are swarmed by bleating cloven workers. They rub and vibrate around you, causing serious burns and emotional damage.",
    "You die by the horns of a goat halfway up the goat tower.",
    "You successfully enter the goat tower.",
    "You talk to the goat master of the goat tower. He imparts upon you great and dark goat wisdom.",
    "The goat herd attacks your girlfriend, taking her hostage and demanding the release of their imprisoned goat brothers.",
    "You learn the secrets of the goat tower.",
    "The goat master welcomes you into his goat concubine circle.",
    "You successfully find the door of the tower, but the door is locked! Can you find the key?",
    "You're a goat, Harry.",
    "You become a goat of the goat tower.",
    "You do some gnarly rad goat shit and the goats are generally stoked on your chill vibe.",
    "The goats of the goat tower give you a massage with their cloven hooves.",
    "You die an old man at the top of the tower, your goat herd surrounding your bed.",
    "You successfully enter the goat tower. Or do you. In patternist Tegmark-4 space you haven't truly entered anything until you've defeated 5 neoreactionaries in midi-to-midi combat.",
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
