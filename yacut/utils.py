import re
import random

from . import CHARACTERS, CHEK_PATTERN, RANDOM_LENGTH


def random_string(length=RANDOM_LENGTH):
    return ''.join(random.choices(CHARACTERS, k=length))


def validate_custom_id(custom_id):
    return bool(re.search(CHEK_PATTERN, custom_id))
