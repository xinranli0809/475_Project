import pygame
import tensorflow as tf
import random as rand
import PIL
import numpy as np
import tkinter as tk
from tkinter import *


def test(fname,model):

    iname = str(fname)
    img = PIL.Image.open(iname)
    img = np.asarray(img)/255.   

    x = img.reshape((1,) + img.shape)
    Prob = newModel.predict(x)
    attrResult = 0
    result = 0
    if np.argmax(Prob) == 1:
        attrResult = 1
    else:
        attrResult = 0
    
    return attrResult

# Image filenames
Nathaniel = 'IMG_5970.jpg'
Sarah = 'IMG_8114.jpg'
David = 'David.jpg'
Hannah = 'test.jpg'
PICTURES = [Nathaniel,Sarah,David,Hannah]
pictures = [Nathaniel,Sarah,David,Hannah]

# Attributes
ATTR= ['Male','Eyeglasses','Wearing_Hat']

# Colors for game background
black = (0,0,0)
white = (255,255,255)
done = False


# Run the game board 
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
    