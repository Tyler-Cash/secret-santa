import random

import database
import user
from santa import add_recipient
from random import shuffle

already_taken = []


def select_random_user(set):
    array = []
    for piece in set:
        array.append(piece)

    size_of_array = len(array) - 1
    rand = random.randint(0, size_of_array)

    return array[rand]


def remove_user(person_ID, origianl_list):
    list = []
    for member in origianl_list:
        if member[1] is not person_ID:
            list.append(member)
    return list


db = database.get_database('database.db')
santas = user.get_from_family(db, 3)
santas = santas + user.get_from_family(db, 2)

shuffle(santas)

recipients = santas
shuffle(recipients)

for santa in santas:
    pair_found = False
    i = 0
    while not pair_found:
        i += 1
        possible_pair = select_random_user(recipients)
        if possible_pair[3] != santa[3] or (i > 250 and possible_pair[1] != santa[1]):
            add_recipient(santa[1], possible_pair[1], db)
            santas = remove_user(santa[1], santas)
            recipients = remove_user(possible_pair[1], recipients)
            pair_found = True
