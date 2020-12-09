import random as rand

class Person:
    def __init__(self, name, ID):
        self.name = name
        self.ID = ID
        self.attribute_dict = dict()

    def __repr__(self):
        return self.name

# People objects
nathaniel = Person('Nathaniel', 'Images/Nathaniel.jpg')
nathaniel.attribute_dict['Male'] = 1
nathaniel.attribute_dict['Eyeglasses'] = 0
nathaniel.attribute_dict['Wearing_hat'] = 1
nathaniel.attribute_dict['Smiling'] = 1
nathaniel.attribute_dict['Blond_Hair'] = 0

sarah = Person('Sarah', 'Images/Sarah.jpg')
sarah.attribute_dict['Male'] = 0
sarah.attribute_dict['Eyeglasses'] = 0
sarah.attribute_dict['Wearing_hat'] = 0
sarah.attribute_dict['Smiling'] = 1
sarah.attribute_dict['Blond_Hair'] = 1

lin = Person('Lin', 'Images/Lin.jpg')
lin.attribute_dict['Male'] = 0
lin.attribute_dict['Eyeglasses'] = 0
lin.attribute_dict['Wearing_hat'] = 1
lin.attribute_dict['Smiling'] = 1
lin.attribute_dict['Blond_Hair'] = 0

xinran = Person('Xinran', 'Images/Xinran.jpg')
xinran.attribute_dict['Male'] = 1
xinran.attribute_dict['Eyeglasses'] = 0
xinran.attribute_dict['Wearing_hat'] = 0
xinran.attribute_dict['Smiling'] = 0
xinran.attribute_dict['Blond_Hair'] = 0

david = Person('David', 'Images/David.jpg')
david.attribute_dict['Male'] = 1
david.attribute_dict['Eyeglasses'] = 0
david.attribute_dict['Wearing_hat'] = 0
david.attribute_dict['Smiling'] = 1
david.attribute_dict['Blond_Hair'] = 1

ilene = Person('Ilene', 'Images/Ilene.jpg')
ilene.attribute_dict['Male'] = 0
ilene.attribute_dict['Eyeglasses'] = 1
ilene.attribute_dict['Wearing_hat'] = 0
ilene.attribute_dict['Smiling'] = 1
ilene.attribute_dict['Blond_Hair'] = 0

emily = Person('Emily', 'Images/Emily.jpg')
emily.attribute_dict['Male'] = 0
emily.attribute_dict['Eyeglasses'] = 1
emily.attribute_dict['Wearing_hat'] = 0
emily.attribute_dict['Smiling'] = 1
emily.attribute_dict['Blond_Hair'] = 1

nik = Person('Nik', 'Images/Nik.jpg')
nik.attribute_dict['Male'] = 1
nik.attribute_dict['Eyeglasses'] = 1
nik.attribute_dict['Wearing_hat'] = 0
nik.attribute_dict['Smiling'] = 0
nik.attribute_dict['Blond_Hair'] = 0


# people library that is unchanged, contains all the people in the game
people_library = [nathaniel, sarah, lin, xinran, david, ilene, emily, nik]
# player 1 (person)'s library of people
player1_people = [nathaniel, sarah, lin, xinran, david, ilene, emily, nik]
# player 2 (computer)'s library of people
player2_people = [nathaniel, sarah, lin, xinran, david, ilene, emily, nik]

player1_attributes = ['Male', 'Eyeglasses', 'Wearing_hat', 'Smiling', 'Blond_Hair']
player2_attributes = ['Male', 'Eyeglasses', 'Wearing_hat', 'Smiling', 'Blond_Hair']

player2_person = sarah

def ifYesPushed(p_list, a_list, guess):
    p_list_new = []
    if len(p_list) == 1:
        p_list_new.append(p_list[0])
        message = 'Is your person ' + p_list[0].name + '?'
    elif len(a_list) == 0:
        message = 'Is your person ' + rand.choice(p_list).name + '?'
    else:
        for person in p_list:
            if person.attribute_dict[guess] == 1:
                p_list_new.append(person)
            else:
                pass
        message = False

    if message:
        print(message)

    return p_list_new, a_list


def ifNoPushed(p_list, a_list, guess):
    p_list_new = []
    if len(p_list) == 1:
        p_list_new.append(p_list[0])
        message = 'Is your person ' + p_list[0].name + '?'
    elif len(a_list) == 0:
        message = 'Is your person ' + rand.choice(p_list).name + '?'
    else:
        for person in p_list:
            if person.attribute_dict[guess] == 0:
                p_list_new.append(person)
            else:
                pass
        message = False

    if message:
        print(message)

    return p_list_new, a_list


def ifMale(p2_person, p1_list, p2_list, a2_list):
    """
    p2_person: player 2 (computer)'s person
    p1_list : player 1's list of people that player 2 can potentially have
    p2_list : player 2's list of people that player 1 can potentially have
    a2_list : player 2's list of attributes that player 1's person can potentially have
    """
    # computer responds yes or no
    p1_list_new = []
    if p2_person.attribute_dict['Male'] == 1:
        message = 'Yes, my person is male'
        # update player 1's list
        for person in p1_list:
            if person.attribute_dict['Male'] == 1:
                p1_list_new.append(person)
            else:
                pass
    else:
        message = 'No, my person is female'
        # update player 1's list
        for person in p1_list:
            if person.attribute_dict['Male'] == 0:
                p1_list_new.append(person)
            else:
                pass
    print(message)

    # computer makes new guess
    att_dict = dict()
    for attribute in a2_list:
        att_dict[attribute] = 0
        for p in p2_list:
            if p.attribute_dict[attribute] == 1:
                att_dict[attribute] += 1
            else:
                pass
    # computer asks if player 1's person has attribute with highest frequency
    max_att = max(att_dict, key=att_dict.get)
    a2_list.remove(max_att)
    message2 = 'Does your person have the attribute ' + max_att + '?'
    print(message2)

    return p1_list_new, a2_list


def ifEyeglasses(p2_person, p1_list, p2_list, a2_list):
    """
    p2_person: player 2 (computer)'s person
    p1_list : player 1's list of people that player 2 can potentially have
    p2_list : player 2's list of people that player 1 can potentially have
    a2_list : player 2's list of attributes that player 1's person can potentially have
    """
    # computer responds yes or no
    p1_list_new = []
    if p2_person.attribute_dict['Eyeglasses'] == 1:
        message = 'Yes, my person is wearing eyeglasses'
        # update player 1's list
        for person in p1_list:
            if person.attribute_dict['Eyeglasses'] == 1:
                p1_list_new.append(person)
            else:
                pass
    else:
        message = 'No, my person is not wearing eyeglasses'
        # update player 1's list
        for person in p1_list:
            if person.attribute_dict['Eyeglasses'] == 0:
                p1_list_new.append(person)
            else:
                pass
    print(message)

    # computer makes new guess
    att_dict = dict()
    for attribute in a2_list:
        att_dict[attribute] = 0
        for p in p2_list:
            if p.attribute_dict[attribute] == 1:
                att_dict[attribute] += 1
            else:
                pass
    # computer asks if player 1's person has attribute with highest frequency
    max_att = max(att_dict, key=att_dict.get)
    a2_list.remove(max_att)
    message2 = 'Does your person have the attribute ' + max_att + '?'
    print(message2)

    return p1_list_new, a2_list


def ifHat(p2_person, p1_list, p2_list, a2_list):
    """
    p2_person: player 2 (computer)'s person
    p1_list : player 1's list of people that player 2 can potentially have
    p2_list : player 2's list of people that player 1 can potentially have
    a2_list : player 2's list of attributes that player 1's person can potentially have
    """
    # computer responds yes or no
    p1_list_new = []
    if p2_person.attribute_dict['Wearing_hat'] == 1:
        message = 'Yes, my person is wearing a hat'
        # update player 1's list
        for person in p1_list:
            if person.attribute_dict['Wearing_hat'] == 1:
                p1_list_new.append(person)
            else:
                pass
    else:
        message = 'No, my person is not wearing a hat'
        # update player 1's list
        for person in p1_list:
            if person.attribute_dict['Wearing_hat'] == 0:
                p1_list_new.append(person)
            else:
                pass
    print(message)

    # computer makes new guess
    att_dict = dict()
    for attribute in a2_list:
        att_dict[attribute] = 0
        for p in p2_list:
            if p.attribute_dict[attribute] == 1:
                att_dict[attribute] += 1
            else:
                pass
    # computer asks if player 1's person has attribute with highest frequency
    max_att = max(att_dict, key=att_dict.get)
    a2_list.remove(max_att)
    message2 = 'Does your person have the attribute ' + max_att + '?'
    print(message2)

    return p1_list_new, a2_list


def ifSmiling(p2_person, p1_list, p2_list, a2_list):
    """
    p2_person: player 2 (computer)'s person
    p1_list : player 1's list of people that player 2 can potentially have
    p2_list : player 2's list of people that player 1 can potentially have
    a2_list : player 2's list of attributes that player 1's person can potentially have
    """
    # computer responds yes or no
    p1_list_new = []
    if p2_person.attribute_dict['Smiling'] == 1:
        message = 'Yes, my person is smiling'
        # update player 1's list
        for person in p1_list:
            if person.attribute_dict['Smiling'] == 1:
                p1_list_new.append(person)
            else:
                pass
    else:
        message = 'No, my person is not smiling'
        # update player 1's list
        for person in p1_list:
            if person.attribute_dict['Smiling'] == 0:
                p1_list_new.append(person)
            else:
                pass
    print(message)

    # computer makes new guess
    att_dict = dict()
    for attribute in a2_list:
        att_dict[attribute] = 0
        for p in p2_list:
            if p.attribute_dict[attribute] == 1:
                att_dict[attribute] += 1
            else:
                pass
    # computer asks if player 1's person has attribute with highest frequency
    max_att = max(att_dict, key=att_dict.get)
    a2_list.remove(max_att)
    message2 = 'Does your person have the attribute ' + max_att + '?'
    print(message2)

    return p1_list_new, a2_list


def ifBlonde(p2_person, p1_list, p2_list, a2_list):
    """
    p2_person: player 2 (computer)'s person
    p1_list : player 1's list of people that player 2 can potentially have
    p2_list : player 2's list of people that player 1 can potentially have
    a2_list : player 2's list of attributes that player 1's person can potentially have
    """
    # computer responds yes or no
    p1_list_new = []
    if p2_person.attribute_dict['Blond_Hair'] == 1:
        message = 'Yes, my person has blonde hair'
        # update player 1's list
        for person in p1_list:
            if person.attribute_dict['Blond_Hair'] == 1:
                p1_list_new.append(person)
            else:
                pass
    else:
        message = 'No, my person does not have blonde hair'
        # update player 1's list
        for person in p1_list:
            if person.attribute_dict['Blond_Hair'] == 0:
                p1_list_new.append(person)
            else:
                pass
    print(message)

    # computer makes new guess
    att_dict = dict()
    for attribute in a2_list:
        att_dict[attribute] = 0
        for p in p2_list:
            if p.attribute_dict[attribute] == 1:
                att_dict[attribute] += 1
            else:
                pass
    # computer asks if player 1's person has attribute with highest frequency
    max_att = max(att_dict, key=att_dict.get)
    a2_list.remove(max_att)
    message2 = 'Does your person have the attribute ' + max_att + '?'
    print(message2)

    return p1_list_new, a2_list
