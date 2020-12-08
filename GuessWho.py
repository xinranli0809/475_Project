import tensorflow as tf
import random as rand
import PIL
import numpy as np
import tkinter as tk
from tkinter import *

class Person:
    def __init__(self, name,ID):
        self.name = name
        self.ID = ID
        self.Male = 0
        self.Eyeglasses = 0
        self.Wearing_hat = 0
        self.Smiling = 0
        self.Blond_Hair = 0

class Attribute:
    def __init__(self, name):
        self.name = name
        self.num  = 0

def classify(fname,model):

    iname = str(fname)
    img = PIL.Image.open(iname)
    img = np.asarray(img)/255.   

    x = img.reshape((1,) + img.shape)
    Prob = model.predict_step(tf.convert_to_tensor(x))
    attrResult = 0
    if np.argmax(Prob) == 1:
        attrResult = 1
    else:
        attrResult = 0
    
    return attrResult

# People objects
nathaniel = Person('Nathaniel')
sarah = Person('Sarah')
lin = Person('Lin')
xinran = Person('Xinran')
david = Person('David')
mom = Person("Sarah's Mom")
roomate = Person("Sarah's Roomate")
nick = Person('Nick')
people = [nathaniel,sarah,lin,xinran,david,mom,roommate,nick]

# Attributes
ATTR = [Attribute('Male'),Attribute('Eyeglasses'),Attribute('Wearing_Hat'),Attribute('Smiling'),Attribute('Blond_Hair')]

# Classify each image

for attr in ATTR:
    # Load the model
    print('Loading pretrained model, this will take a while (~30 sec to 1 min)')
    # this can be speed up by only saving and loading the weights, maybe
    newModel = newModel = loadModel(attr.name)
    print('Model loaded')

    for person in people:
        result = classify(person.ID,newModel)
        if result == 1:
            attr.num += 1
            setattr(person,attr.name,1)


# Run the game board 
done = False
while not done:

    if len(pictures) == 1:
        print('The person is ' + pictures[0])
        done = True
    elif len(ATTR) == 0:
        num = rand.choice(range(len(pictures)))
        pic = pictures.pop(num)
        text = input('Is the person ' + pic + '?' + '(y/n)\n')
        if text == 'y':
            print('The person is ' + pic)
        else:
            continue
        

    # Select the Attribute
    num = rand.choice(range(len(ATTR)))
    attribute = ATTR.pop(num)

    print('Loading pretrained model, this will take a while (~30 sec to 1 min)')
    # this can be speed up by only saving and loading the weights, maybe
    newModel = tf.keras.models.load_model('./' + attribute,compile=False)
    print('Model loaded')

    # Que the user for clue
    text = input('Does the user have the attribute ' + attribute + '(y/n):\n')
    if text == 'y':
        ans = 1
    else:
        ans = 0

    # Evaluate each picture
    for pic in pictures:
        result = test(pic,newModel)
        if ans != result:
            pictures.remove(pic)
    