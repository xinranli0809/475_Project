#import pygame
#import tensorflow as tf
import random as rand
import PIL.Image
import PIL.ImageTk
import numpy as np
import tkinter as tk
from tkinter import Label
from tkinter import font as tkfont


main = tk.Tk()

mframe = tk.Frame(main)
mframe.grid(row=0,column=0)

# specify where window will open (50 points to the left and 50 points down from the top-left corner)
main.geometry("+50+50")

# prevent player from resizing window 
main.resizable(width=False,height=False)


################################################################################################################################
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


################################################################################################################################
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


###########################################################################################################################################
# function that gets called if the yes button is pushed
def ifYesPushed(guess):
    """
    guessed_attribute : the attribute that player 2 guessed
    """

    # if there is one more person in player 2's list
    if len(player2_people) == 1:
        message = 'Is your person ' + player2_people[0].name + '?'
    # if there are no more attributes left to guess
    elif len(player2_attributes) == 0:
        message = 'Is your person ' + rand.choice(player2_people[0].name + '?')
    else:
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

        max_att = max(att_dict, key=att_dict.get)
        message = 'Does your person have the attribute, ' + max_att + '?'
        player2_attributes.remove(max_att)
    #pass
    return message

# function that gets called if the yes button is pushed
def ifNoPushed(guess):
    """
    guessed_attribute : the attribute that player 2 guessed
    """

    # if there is one more person in player 2's list
    if len(player2_people) == 1:
        message = 'Is your person ' + player2_people[0].name + '?'
    # if there are no more attributes left to guess
    elif len(player2_attributes) == 0:
        message = 'Is your person ' + rand.choice(player2_people[0].name + '?')
    else:
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

        max_att = max(att_dict, key=att_dict.get)
        message = 'Does your person have the attribute, ' + max_att + '?'
        player2_attributes.remove(max_att)
    #print(message)
    #pass
    return message

guessed_attribute = 'Male'


###########################################################################################################################################
# Clear the main windows frame of all widgets
def clearwin():
    for child in mframe.winfo_children():
        child.destroy()
    mframe.pack_forget()
    mframe.grid_forget()
        #child.pack_forget()
        #child.forget()
        #child.grid_forget

def win1():
    '''Create the main window'''
    clearwin()

    # define title font style 
    title_font = tkfont.Font(family='Helvetica', size=30, weight="bold")

    # define text at top of page 
    label = tk.Label(text="Guess Who?", font=title_font)
    label.grid(row=1,column=0) #(side="top", fill="x", pady=10)

    # add game instructions 
    # font
    instructFont = tkfont.Font(family='Helvetica', size=12)
    instructtext = "Instructions on how to play the game once we decide on those.. blah blah blah more stuff"
    instructtext = instructtext + " and more and more and more"
    instructlabel = tk.Label(text=instructtext,font=instructFont)
    instructlabel.grid(row=2,column=0) #pack(pady=10)

    # button to start the game, green background with white words 
    # buton font 
    buttonfont = tkfont.Font(family='Helvetica', size=12, weight="bold")
    button = tk.Button(text="Begin Game", height=2, width=15,bg='#099412', fg='#ffffff',
        command=win2,font=buttonfont)
    button.grid(row=3,column=0) #pack(pady=10)

    # add project and creators label 
    botFont = tkfont.Font(family='Helvetica', size=11)
    creatrlabel = tk.Label(text="Xinran Li, Lin Liu, Nathaniel Nyberg, Sarah Ziselman",font=botFont)
    creatrlabel.grid(row=4,column=0) #pack(pady=15)
    projlabel = tk.Label(text="ELEC_ENG_475: Machine Learning: Foundations, Applications, and Algorithms Final Project",font=botFont)
    projlabel.grid(row=5,column=0) #pack()


###########################################################################################################################################
# create game window
def win2():
    clearwin()

    # define font style for the questions
    qfont = tkfont.Font(family='Helvetica', size=12)

    

    # text box where the computer will communicate with the player, scrolls so older messages will be higher up 
    textbox = Label(height=8,width=100)

    # put on grid 
    textbox.grid(row=3, column=0,columnspan=4)

    # initial question 
    textbox["text"] = "Choose your person"
    textbox["font"] = qfont

    ###########################################################################################################################################
    # function to load the pictures and place them in a 2x4 grid
    def loadAndPlacePics(): 
        # load in the pictures and resize them 
        pic1 = PIL.Image.open("Images/David.jpg")
        pic1 = pic1.resize((170,252), PIL.Image.ANTIALIAS)
        render1 = PIL.ImageTk.PhotoImage(pic1)

        pic2 = PIL.Image.open("Images/Lin.jpg")
        pic2 = pic2.resize((170,252), PIL.Image.ANTIALIAS)
        render2 = PIL.ImageTk.PhotoImage(pic2)

        pic3 = PIL.Image.open("Images/Mom.jpg")
        pic3 = pic3.resize((170,252), PIL.Image.ANTIALIAS)
        render3 = PIL.ImageTk.PhotoImage(pic3)

        pic4 = PIL.Image.open("Images/Nathaniel.jpg")
        pic4 = pic4.resize((170,252), PIL.Image.ANTIALIAS)
        render4 = PIL.ImageTk.PhotoImage(pic4)

        pic5 = PIL.Image.open("Images/Nick.jpg")
        pic5 = pic5.resize((170,252), PIL.Image.ANTIALIAS)
        render5 = PIL.ImageTk.PhotoImage(pic5)

        pic6 = PIL.Image.open("Images/Roomate.jpg")
        pic6 = pic6.resize((170,252), PIL.Image.ANTIALIAS)
        render6 = PIL.ImageTk.PhotoImage(pic6)

        pic7 = PIL.Image.open("Images/Sarah.jpg")
        pic7 = pic7.resize((170,252), PIL.Image.ANTIALIAS)
        render7 = PIL.ImageTk.PhotoImage(pic7)

        pic8 = PIL.Image.open("Images/Xinran.jpg")
        pic8 = pic8.resize((170,252), PIL.Image.ANTIALIAS)
        render8 = PIL.ImageTk.PhotoImage(pic8)
        

        # callback functions for all picture buttons 
        def p1Push():
            # wait a 0.25second before displaying the message
            main.after(250)
            textbox["text"]="You have chosen David. Push Yes to start the game or choose another person"
            textbox["font"]=qfont

        def p2Push():
            # wait a 0.25second before displaying the message
            main.after(250)
            textbox["text"]="You have chosen Lin. Push Yes to start the game or choose another person"
            textbox["font"]=qfont

        def p3Push():
            # wait a 0.25second before displaying the message
            main.after(250)
            textbox["text"]="You have chosen Ilene. Push Yes to start the game or choose another person"
            textbox["font"]=qfont

        def p4Push():
            # wait a 0.25second before displaying the message
            main.after(250)
            textbox["text"]="You have chosen Nathaniel. Push Yes to start the game or choose another person"
            textbox["font"]=qfont

        def p5Push():
            # wait a 0.25second before displaying the message
            main.after(250)
            textbox["text"]="You have chosen Nik. Push Yes to start the game or choose another person"
            textbox["font"]=qfont

        def p6Push():
            # wait a 0.25second before displaying the message
            main.after(250)
            textbox["text"]="You have chosen Emily. Push Yes to start the game or choose another person"
            textbox["font"]=qfont

        def p7Push():
            # wait a 0.25second before displaying the message
            main.after(250)
            textbox["text"]="You have chosen Sarah. Push Yes to start the game or choose another person"
            textbox["font"]=qfont

        def p8Push():
            # wait a 0.25second before displaying the message
            main.after(250)
            textbox["text"]="You have chosen Xinran. Push Yes to start the game or choose another person"
            textbox["font"]=qfont


        # make images into buttons and place the images on a 2x4 grid with borders along x and y to space out the pictures 
        img1 = tk.Button(main,image=render1,command=p1Push)
        img1.image = render1
        img1.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        img2 = tk.Button(main,image=render2,command=p2Push)
        img2.image = render2
        img2.grid(row=0, column=1, padx=5, pady=5)

        img3 = tk.Button(main,image=render3,command=p3Push)
        img3.image = render3
        img3.grid(row=0, column=2, padx=5, pady=5)

        img4 = tk.Button(main,image=render4,command=p4Push)
        img4.image = render4
        img4.grid(row=0, column=3, padx=5, pady=5)

        img5 = tk.Button(main,image=render5,command=p5Push)
        img5.image = render5
        img5.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        img6 = tk.Button(main,image=render6,command=p6Push)
        img6.image = render6
        img6.grid(row=1, column=1, padx=5, pady=5)

        img7 = tk.Button(main,image=render7,command=p7Push)
        img7.image = render7
        img7.grid(row=1, column=2, padx=5, pady=5)
        
        img8 = tk.Button(main,image=render8,command=p8Push)
        img8.image = render8
        img8.grid(row=1, column=3, padx=5, pady=5)
    

    # load and place pictures 
    loadAndPlacePics()

    ###########################################################################################################################################
    # function that gives a value if the button has been pushed
    def YesisPushed():
        #print("pushed")
        msg=ifYesPushed(guessed_attribute)

        # wait a 0.25second before displaying the new question 
        main.after(250)
        textbox["text"]=msg
        textbox["font"]=qfont
        

    # function that gives a value if the button has been pushed
    def NoisPushed():
        #print("pushed")
        msg = ifNoPushed(guessed_attribute)

        # wait a 0.25second before displaying the new question 
        main.after(250)
        textbox["text"]=msg
        textbox["font"]=qfont
    ############################################################################################################################################


    # buttons for yes and no response  
    buttonfont = tkfont.Font(family='Helvetica', size=12, weight="bold")

    # yes button with green background and white text
    yesbutton = tk.Button(main,text="Yes", height=1, width=10,bg='#099412', fg='#ffffff',font=buttonfont,command=YesisPushed)
    yesbutton.grid(row=4,column=1,padx=10,pady=15,sticky="n")

    # no button with red background and white text 
    nobutton = tk.Button(main,text="No", height=1, width=10,bg='#ab0a0a', fg='#ffffff',font=buttonfont,command=NoisPushed)
    nobutton.grid(row=4,column=2,padx=10,pady=15,sticky="n")   

win2()
main.mainloop()

