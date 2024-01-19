import re
import random

from . import CHARACTERS


def random_string():
    return ''.join(random.choices(CHARACTERS, k=6))


def check_custom(custom_id):
    return True if re.search(r'^[A-Za-z0-9]{,6}$', custom_id) else False
