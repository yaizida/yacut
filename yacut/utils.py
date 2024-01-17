import random
import string

CHARACTERS = string.ascii_letters + string.digits


def random_string():
    random_id = ''
    for _ in range(6):
        random_id += random.choice(CHARACTERS)
    return random_id


def check_custom(custom_id):
    # На сколько релевнтно здесь реализоывть Бинарный поиск?
    for symbol in custom_id:
        if symbol not in CHARACTERS:
            return False
    return True
    
