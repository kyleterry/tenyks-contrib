def run(data, settings):
    if data['payload'].startswith('is it wednesday'):
        mydude = 'https://www.youtube.com/watch?v=EBNEPil4da0&list=PLy3-VH7qrUZ5IVq_lISnoccVIYZCMvi-8'
    else:
        mydude = 'no'

    return '{nick}: {mydude}'.format(nick=data['nick'], 
            mydude=mydude)

