import re
import random

from . import CHARACTERS, CHEK_PATTERN


def random_string(length=6):
    return ''.join(random.choices(CHARACTERS, k=length))


def validate_custom_id(custom_id):
    return True if re.search(CHEK_PATTERN, custom_id) else False
