import json
from random import randint


def getRandomUa():
    # Open ua file
    with open('uarandom.json', 'r') as ua:
        ua = json.load(ua)
    MAX_LEN = len(ua)
    rand_index = randint(0, (MAX_LEN - 1))
    return ua[rand_index]

def getIndexUa(index):
    # Open ua file
    with open('uarandom.json', 'r') as ua:
        ua = json.load(ua)
    try:
        user = ua[index]
    except Exception:
        user = ua[0]
    return user
