import random
import string


def random_string(length=10):
    characters = string.ascii_letters + string.digits
    random_id = ''
    for _ in range(length):
        random_id += random.choice(characters)
    return random_id
