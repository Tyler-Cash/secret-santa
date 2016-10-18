import random

import database
import user
import santa


def select_random_user(set):
    array = []
    for piece in set:
        array.append(piece[1])

    sizeOfArray = len(array) - 1
    rand = random.randint(0, sizeOfArray)

    print(rand)
    return array[rand]


def removeUser(person_ID, origianl_list):
    list = []
    for member in origianl_list:
        if member[1] is not person_ID:
            list.append(member)
    return list

db = database.get_database('database.db')
family1 = user.get_from_family(db,1)
family2 = user.get_from_family(db, 2)
for user in family1:
    rand_person = select_random_user(family2)
    santa.add_recipient(user[1], rand_person,db)
    family2 = removeUser(rand_person, family2)