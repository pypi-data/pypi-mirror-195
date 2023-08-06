import re

REGEX_KEY = "^sk-[A-Za-z0-9-]{48}$"

def is_valid_key(key):
    return re.search(REGEX_KEY, key)