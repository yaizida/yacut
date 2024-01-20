import re
import random

from . import CHARACTERS


def random_string(length=6):
    return ''.join(random.choices(CHARACTERS, k=length))


def validate_custom_id(custom_id):
    return True if re.search(r'^[A-Za-z0-9]{,16}$', custom_id) else False
