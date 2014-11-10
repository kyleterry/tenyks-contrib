import random

def run(data, settings):
    if data['payload'] == 'goat thrower':
        if random.randint(0, 110) == 0:
            outcome = random.randint(0, 2)
            if outcome == 0:
                return "{nick}: The goat thrower engulfs you in a billowing wave of goat. Goats swim over your body as they reduce your flesh to a blackened pile of goat feces.".format(nick = data['nick'])
            else:
                return "{nick}: The goat thrower issues a stream of goats out onto the bushlands. The goats spread all over the forest, causing an irreversable reduction in biodiversity.".format(nick = data['nick'])
        else:
            distance = random.randrange(0, 100)
            num_goats = random.randrange(1, 5)
            judgement = ""
            if distance < 25:
                judgement = "Fucking awful."
            elif distance < 50:
                judgement = "Try to do better next time."
            elif distance < 75:
                judgement = "Not bad. I've seen better."
            elif distance < 100:
                judgement = "Nice throw, idiot. Why are you throwing goats?"
            else:
                judgement = "Calm down, kingpin"

            return '{nick}: You manage to heave {num_goats} goats for {distance}M. {judgement}'.format(
                    nick = data['nick'],
                    num_goats = num_goats,
                    distance = distance,
                    judgement = judgement
            )
