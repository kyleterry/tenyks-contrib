import random

def run(data, settings):
    if data['payload'] == 'goat thrower':
        distance = random.randrange(0, 100)
        num_goats = random.randrange(1, 5)
        judgement = ""
        if distance == 0:
            judgement = "Fucking awful."
        elif distance > 25 and distance < 50:
            judgement = "Try to do better next time."
        elif distance > 50 and distance < 75:
            judgement = "Not bad. I've seen better."
        elif distance > 75 and distance < 100:
            judgement = "Nice throw, idiot. Why are you throwing goats?"
        elif distance == 100:
            judgement = "Calm down, kingpin"

        say = '{nick}: You manage to heave {num_goats} goats for {distance}M. {judgement}'.format(
                nick = data['nick'],
                num_goats = num_goats,
                distance = distance,
                judgement = judgement
        )
        return say
