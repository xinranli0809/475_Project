import tensorflow as tf
import random as rand
import PIL
import numpy as np
import tkinter as tk
from tkinter import *


class Person:
    def __init__(self, name, ID):
        self.name = name
        self.ID = ID
        self.attribute_dict = dict()
        # self.Male = 0
        # self.Eyeglasses = 0
        # self.Wearing_hat = 0
        # self.Smiling = 0
        # self.Blond_Hair = 0

    def __repr__(self):
        return self.name


class Attribute:
    def __init__(self, name):
        self.name = name
        self.num = 0


def classify(fname, model):
    iname = str(fname)
    img = PIL.Image.open(iname)
    img = np.asarray(img) / 255.

    x = img.reshape((1,) + img.shape)
    Prob = model.predict_step(tf.convert_to_tensor(x))
    attrResult = 0
    if np.argmax(Prob) == 1:
        attrResult = 1
    else:
        attrResult = 0

    return attrResult


########################################################################################
# I adjusted the names of people, the file paths and created lists for each player

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
david.attribute_dict['Smiling'] = 0
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
# Attributes

Male = Attribute('Male')
Eyeglasses = Attribute('Eyeglasses')
Wearing_hat = Attribute('Wearing_hat')
Smiling = Attribute('Smiling')
Blond_Hair = Attribute('Blond_Hair')

# ATTR = [Male, Eyeglasses, Wearing_hat, Smiling, Blond_Hair]
# player1_attributes = [Male, Eyeglasses, Wearing_hat, Smiling, Blond_Hair]
# player2_attributes = [Male, Eyeglasses, Wearing_hat, Smiling, Blond_Hair]
ATTR = ['Male', 'Eyeglasses', 'Wearing_hat', 'Smiling', 'Blond_Hair']
player1_attributes = ['Male', 'Eyeglasses', 'Wearing_hat', 'Smiling', 'Blond_Hair']
player2_attributes = ['Male', 'Eyeglasses', 'Wearing_hat', 'Smiling', 'Blond_Hair']

# comment this out when actually using the model to classify the images
# this was hardcoded in to test the UI
# nathaniel.Male = 1
# nathaniel.Wearing_hat = 1
# nathaniel.Smiling = 1
# sarah.Smiling = 1
# sarah.Blond_Hair = 1
# lin.Wearing_hat = 1
# lin.Smiling = 1
# xinran.Male = 1
# david.Male = 1
# david.Smiling = 1
# ilene.Eyeglasses = 1
# ilene.Smiling = 1
# emily.Eyeglasses = 1
# emily.Smiling = 1
# emily.Blond_Hair = 1
# nik.Male = 1
# nik.Eyeglasses = 1
###########################################################################################################

# Classify each image

# for attr in ATTR:
#     # Load the model
#     print('Loading pretrained model, this will take a while (~30 sec to 1 min)')
#     # this can be speed up by only saving and loading the weights, maybe
#     newModel = loadModel(attr.name)
#     print('Model loaded')
#
#     for person in people_library:
#         result = classify(person.ID, newModel)
#         if result == 1:
#             attr.num += 1
#             setattr(person, attr.name, 1)

# Run the game board
done = False


##############################################################################
# These are the functions I created

# function that gets called if the yes button is pushed
def ifYesPushed(guess):
    """
    guessed_attribute : the attribute that player 2 guessed
    """

    # checks through player 2's list for people with the attribute
    for p in player2_people:
        if p.attribute_dict[guess] == 0:
            player2_people.remove(p)
        else:
            pass

    # player 2 (computer) looks for attribute with highest frequency
    # creates empty dictionary to save # of images with attribute
    att_dict = dict()
    # loops through remaining attributes
    for a in player2_attributes:
        att_dict[a] = 0
        # loops through remaining people
        for b in player2_people:
            if b.attribute_dict[a] == 1:
                att_dict[a] += 1
            else:
                pass

    max_att = max(att_dict, key = att_dict.get)
    message = 'Does your person have the attribute, ' + max_att + '?'
    pass

# function that gets called if the yes button is pushed
def ifNoPushed(guess):
    """
    guessed_attribute : the attribute that player 2 guessed
    """

    # checks through player 2's list for people with the attribute
    for p in player2_people:
        if p.attribute_dict[guess] == 1:
            player2_people.remove(p)
        else:
            pass

    # player 2 (computer) looks for attribute with highest frequency
    # creates empty dictionary to save # of images with attribute
    att_dict = dict()
    # loops through remaining attributes
    for a in player2_attributes:
        att_dict[a] = 0
        # loops through remaining people
        for b in player2_people:
            if b.attribute_dict[a] == 1:
                att_dict[a] += 1
            else:
                pass

    max_att = max(att_dict, key = att_dict.get)
    message = 'Does your person have the attribute, ' + max_att + '?'
    pass

guessed_attribute = 'Male'
ifNoPushed(guessed_attribute)

###########################################################################################

# while not done:
#     # person for player 1 is randomly selected
#     player1_person = rand.choice(people_library)
#     # person for player 2 is randomly selected from list of remaining people
#     remaining_people = people_library.remove(player1_person)
#     player2_person = rand.choice(remaining_people)
#
#     if len(player2_people) == 1:
#         print('The person is ' + player2_people[0])
#         done = True
#     elif len(ATTR) == 0:
#         num = rand.choice(range(len(player2_people)))
#         pic = player2_people.pop(num)
#         text = input('Is the person ' + pic + '?' + '(y/n)\n')
#         if text == 'y':
#             print('The person is ' + pic)
#         else:
#             continue
#
#     # Select the Attribute
#     num = rand.choice(range(len(ATTR)))
#     attribute = ATTR.pop(num)
#
#     print('Loading pretrained model, this will take a while (~30 sec to 1 min)')
#     # this can be speed up by only saving and loading the weights, maybe
#     newModel = tf.keras.models.load_model('./' + attribute, compile=False)
#     print('Model loaded')
#
#     # Que the user for clue
#     text = input('Does the user have the attribute ' + attribute + '(y/n):\n')
#     if text == 'y':
#         ans = 1
#     else:
#         ans = 0
#
#     # Evaluate each picture
#     for pic in people_library:
#         result = test(pic, newModel)
#         if ans != result:
#             people_library.remove(pic)