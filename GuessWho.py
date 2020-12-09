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

# name the window
main.title("Guess Who Game")

mframe = tk.Frame(main)
mframe.grid(row=0,column=0)

# specify where window will open (50 points to the left and 50 points down from the top-left corner)
main.geometry("+50+50")

# prevent player from resizing window 
main.resizable(width=False,height=False)

# keep track if the game started or not, will be 1 if it's started 
gamestart = 0

# see if the computer guessed your person correctly, =1 will check 
checkguess = 0

# for the first window to completely delete it 
win1labels = []


################################################################################################################################
class Person:
    def __init__(self, name, ID):
        self.name = name
        self.ID = ID
        self.attribute_dict = dict()

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

# computer randomly chooses a person 
player2_person = rand.choice(people_library)

###########################################################################################################################################
# function that gets called if the yes button is pushed
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
        message = 0
    #if message:
    #    print(message)
    return message, p_list_new, a_list


# function that gets called if the yes button is pushed
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
        message = 0
    if message:
        print(message)
    return message, p_list_new, a_list


# first attribute to be guessed 
guess = 'Male'

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
    #print(message)

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
    #print(message2)
    return message, message2, p1_list_new, a2_list

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
    #print(message)

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
    #print(message2)

    return message, message2, p1_list_new, a2_list

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
    #print(message)

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
    #print(message2)

    return message, message2, p1_list_new, a2_list

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
    #print(message)

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
    #print(message2)

    return message, message2, p1_list_new, a2_list

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
    #print(message)

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
    #print(message2)

    return message, message2, p1_list_new, a2_list



###########################################################################################################################################
# Clear the main windows frame of all widgets
def clearwin():
    for child in mframe.winfo_children():
        child.grid_remove()
        child.destroy()
    for l in win1labels:
        l.destroy()
        
    mframe.pack_forget()
    mframe.grid_forget()


def win1():
    '''Create the main window'''
    clearwin()

    # define title font style 
    title_font = tkfont.Font(family='Century Gothic', size=30, weight="bold")

    # define text at top of page 
    label = tk.Label(text="Guess Who?", font=title_font)
    label.grid(row=1,column=0) #(side="top", fill="x", pady=10)
    win1labels.append(label)

    # add game instructions 
    # font
    instructFont = tkfont.Font(family='Century Gothic', size=14)
    instructtext = "How to Play the Game:" +'\n'
    instructtext = instructtext + "Just like the classic Guess Who Game." +'\n'
    instructtext = instructtext+ "You will pick a person by clicking on their picture and the computer will randomly pick a person." +'\n'
    instructtext = instructtext + "At the very end click on one of the names to guess the computer's person. Have fun!"
    instructlabel = tk.Label(text=instructtext,font=instructFont)
    instructlabel.grid(row=2,column=0,pady=20,padx=15)
    win1labels.append(instructlabel)

    # button to start the game, green background with white words 
    # buton font 
    buttonfont = tkfont.Font(family='Century Gothic', size=12, weight="bold")
    button = tk.Button(text="Begin Game", height=2, width=15,bg='#099412', fg='#ffffff',
        command=win2,font=buttonfont)
    button.grid(row=3,column=0) #pack(pady=10)
    win1labels.append(button)

    # spacer to look nicer 
    spacer1 = Label(text=" ")
    spacer1.grid(row=4)

    # add project and creators label 
    botFont = tkfont.Font(family='Century Gothic', size=11)
    creatrlabel = tk.Label(text="Xinran Li, Lin Liu, Nathaniel Nyberg, Sarah Ziselman",font=botFont)
    creatrlabel.grid(row=5,column=0,pady=5)

    win1labels.append(creatrlabel)
    projlabel = tk.Label(text="ELEC_ENG_475: Machine Learning: Foundations, Applications, and Algorithms Final Project",font=botFont)
    projlabel.grid(row=6,column=0,pady=10) 
    win1labels.append(projlabel)


###########################################################################################################################################
# create game window
def win2():
    clearwin()

    # define font style for the questions
    qfont = tkfont.Font(family='Century Gothic', size=12)

    # define font style for the attributes title
    attfont = tkfont.Font(family='Century Gothic', size=12, weight="bold")

    # left side of the screen
    leftFrame = tk.Frame()
    leftFrame.grid(row=0,column=0)

    # right side of the screen 
    rightFrame = tk.Frame()
    rightFrame.grid(row=0,column=1)

    # bottom side of the screen 
    botFrame = tk.Frame()
    botFrame.grid(row=1,column=0, columnspan=2)

    # text box where the computer will communicate with the player, scrolls so older messages will be higher up 
    textbox = Label(botFrame,height=5,width=100)

    # put on grid 
    textbox.grid(row=3, column=0,columnspan=4)

    # initial question 
    textbox["text"] = "choose a person and click on their picture. Then click on an attribute to the right to guess the computer's person"
    textbox["font"] = qfont

    ###########################################################################################################################################
    # function to load the pictures and place them in a 2x4 grid
    def loadAndPlacePics(): 
        # load in the pictures and resize them 
        pic1 = PIL.Image.open("Images/David.jpg")
        #pic1 = pic1.resize((170,252), PIL.Image.ANTIALIAS)
        render1 = PIL.ImageTk.PhotoImage(pic1)

        pic2 = PIL.Image.open("Images/Lin.jpg")
        #pic2 = pic2.resize((170,252), PIL.Image.ANTIALIAS)
        render2 = PIL.ImageTk.PhotoImage(pic2)

        pic3 = PIL.Image.open("Images/Mom.jpg")
        #pic3 = pic3.resize((170,252), PIL.Image.ANTIALIAS)
        render3 = PIL.ImageTk.PhotoImage(pic3)

        pic4 = PIL.Image.open("Images/Nathaniel.jpg")
        #pic4 = pic4.resize((170,252), PIL.Image.ANTIALIAS)
        render4 = PIL.ImageTk.PhotoImage(pic4)

        pic5 = PIL.Image.open("Images/Nick.jpg")
        #pic5 = pic5.resize((170,252), PIL.Image.ANTIALIAS)
        render5 = PIL.ImageTk.PhotoImage(pic5)

        pic6 = PIL.Image.open("Images/Roomate.jpg")
        #pic6 = pic6.resize((170,252), PIL.Image.ANTIALIAS)
        render6 = PIL.ImageTk.PhotoImage(pic6)

        pic7 = PIL.Image.open("Images/Sarah.jpg")
        #pic7 = pic7.resize((170,252), PIL.Image.ANTIALIAS)
        render7 = PIL.ImageTk.PhotoImage(pic7)

        pic8 = PIL.Image.open("Images/Xinran.jpg")
        #pic8 = pic8.resize((170,252), PIL.Image.ANTIALIAS)
        render8 = PIL.ImageTk.PhotoImage(pic8)

        xpic = PIL.Image.open("Images/x.jpg")
        #xpic = xpic.resize((170,252), PIL.Image.ANTIALIAS)
        xrender = PIL.ImageTk.PhotoImage(xpic)
        

        # callback functions for all picture buttons 
        def p1Push():
            # take picture away
            if gamestart==1:
                img1['image']=xrender
            else:
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You have chosen David or click on another picture to choose someone else"
                textbox["font"]=qfont
                
                pic1 = PIL.Image.open("Images/David.jpg")
                #pic1 = pic1.resize((170,252), PIL.Image.ANTIALIAS)
                crend = PIL.ImageTk.PhotoImage(pic1)
                cimg = tk.Label(rightFrame,image=crend)
                cimg.image = crend
                cimg.grid(row=7, column=0, padx=5, pady=5)
            
        def name1Push():
            if player2_person==david: 
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You are correct! I chose David."
                textbox["font"]=qfont
            else:
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You are wrong. I didn't chose David."
                textbox["font"]=qfont               

        def p2Push():
            # take picture away
            if gamestart==1:
                img2['image']=xrender
            else:
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You have chosen Lin or click on another picture to choose someone else"
                textbox["font"]=qfont

                pic1 = PIL.Image.open("Images/Lin.jpg")
                #pic1 = pic1.resize((170,252), PIL.Image.ANTIALIAS)
                crend = PIL.ImageTk.PhotoImage(pic1)
                cimg = tk.Label(rightFrame,image=crend)
                cimg.image = crend
                cimg.grid(row=7, column=0, padx=5, pady=5)
        
        def name2Push():
            if player2_person==lin: 
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You are correct! I chose Lin."
                textbox["font"]=qfont
            else:
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You are wrong. I didn't chose Lin."
                textbox["font"]=qfont   

        def p3Push():
            # take picture away
            if gamestart==1:
                img3['image']=xrender
            else:
                 # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You have chosen Ilene or click on another picture to choose someone else"
                textbox["font"]=qfont

                pic1 = PIL.Image.open("Images/Mom.jpg")
                #pic1 = pic1.resize((170,252), PIL.Image.ANTIALIAS)
                crend = PIL.ImageTk.PhotoImage(pic1)
                cimg = tk.Label(rightFrame,image=crend)
                cimg.image = crend
                cimg.grid(row=7, column=0, padx=5, pady=5)

        def name3Push():
            if player2_person==ilene: 
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You are correct! I chose Ilene."
                textbox["font"]=qfont
            else:
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You are wrong. I didn't chose Ilene."
                textbox["font"]=qfont   

        def p4Push():
            # take picture away
            if gamestart==1:
                img4['image']=xrender
            else:
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You have chosen Nathaniel or click on another picture to choose someone else"
                textbox["font"]=qfont

                pic1 = PIL.Image.open("Images/Nathaniel.jpg")
                #pic1 = pic1.resize((170,252), PIL.Image.ANTIALIAS)
                crend = PIL.ImageTk.PhotoImage(pic1)
                cimg = tk.Label(rightFrame,image=crend)
                cimg.image = crend
                cimg.grid(row=7, column=0, padx=5, pady=5)

        def name4Push():
            if player2_person==nathaniel: 
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You are correct! I chose Nathaniel."
                textbox["font"]=qfont
            else:
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You are wrong. I didn't chose Nathaniel."
                textbox["font"]=qfont   

        def p5Push():
            # take picture away
            if gamestart==1:
                img5['image']=xrender
            else:
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You have chosen Nik or click on another picture to choose someone else"
                textbox["font"]=qfont

                pic1 = PIL.Image.open("Images/Nick.jpg")
                #pic1 = pic1.resize((170,252), PIL.Image.ANTIALIAS)
                crend = PIL.ImageTk.PhotoImage(pic1)
                cimg = tk.Label(rightFrame,image=crend)
                cimg.image = crend
                cimg.grid(row=7, column=0, padx=5, pady=5)

        def name5Push():
            if player2_person==nik: 
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You are correct! I chose Nik."
                textbox["font"]=qfont
            else:
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You are wrong. I didn't chose Nik."
                textbox["font"]=qfont   

        def p6Push():
            # take picture away
            if gamestart==1:
                img6['image']=xrender
            else:
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You have chosen Emily or click on another picture to choose someone else"
                textbox["font"]=qfont

                pic1 = PIL.Image.open("Images/Roomate.jpg")
                #pic1 = pic1.resize((170,252), PIL.Image.ANTIALIAS)
                crend = PIL.ImageTk.PhotoImage(pic1)
                cimg = tk.Label(rightFrame,image=crend)
                cimg.image = crend
                cimg.grid(row=7, column=0, padx=5, pady=5)

        def name6Push():
            if player2_person==emily: 
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You are correct! I chose Emily."
                textbox["font"]=qfont
            else:
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You are wrong. I didn't chose Emily."
                textbox["font"]=qfont   

        def p7Push():
            # take picture away
            if gamestart==1:
                img7['image']=xrender
            else:
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You have chosen Sarah or click on another picture to choose someone else"
                textbox["font"]=qfont

                pic1 = PIL.Image.open("Images/Sarah.jpg")
                #pic1 = pic1.resize((170,252), PIL.Image.ANTIALIAS)
                crend = PIL.ImageTk.PhotoImage(pic1)
                cimg = tk.Label(rightFrame,image=crend)
                cimg.image = crend
                cimg.grid(row=7, column=0, padx=5, pady=5)

        def name7Push():
            if player2_person==sarah: 
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You are correct! I chose Sarah."
                textbox["font"]=qfont
            else:
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You are wrong. I didn't chose Sarah."
                textbox["font"]=qfont   

        def p8Push():
            # take picture away
            if gamestart==1:
                img8['image']=xrender
            else:
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You have chosen Xinran or click on another picture to choose someone else"
                textbox["font"]=qfont

                pic1 = PIL.Image.open("Images/Xinran.jpg")
                #pic1 = pic1.resize((170,252), PIL.Image.ANTIALIAS)
                crend = PIL.ImageTk.PhotoImage(pic1)
                cimg = tk.Label(rightFrame,image=crend)
                cimg.image = crend
                cimg.grid(row=7, column=0, padx=5, pady=5)

        def name8Push():
            if player2_person==xinran: 
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You are correct! I chose Xinran."
                textbox["font"]=qfont
            else:
                # wait a 0.25second before displaying the message
                main.after(250)
                textbox["text"]="You are wrong. I didn't chose Xinran."
                textbox["font"]=qfont   


        # make images into buttons and place the images on a 2x4 grid with borders along x and y to space out the pictures 
        img1 = tk.Button(leftFrame,image=render1,command=p1Push)
        img1.image = render1
        img1.grid(row=2, column=0, padx=5, pady=5)
        # label the picture 
        it1 = tk.Button(leftFrame, text="David", font=attfont,command=name1Push)
        it1.grid(row=1, column=0)

        img2 = tk.Button(leftFrame,image=render2,command=p2Push)
        img2.image = render2
        img2.grid(row=2, column=1, padx=5, pady=5)
        # label the picture 
        it2 = tk.Button(leftFrame, text="Lin", font=attfont,command=name2Push)
        it2.grid(row=1, column=1)

        img3 = tk.Button(leftFrame,image=render3,command=p3Push)
        img3.image = render3
        img3.grid(row=2, column=2, padx=5, pady=5)
        # label the picture 
        it3 = tk.Button(leftFrame, text="Ilene", font=attfont,command=name3Push)
        it3.grid(row=1, column=2)

        img4 = tk.Button(leftFrame,image=render4,command=p4Push)
        img4.image = render4
        img4.grid(row=2, column=3, padx=5, pady=5)
        # label the picture 
        it4 = tk.Button(leftFrame, text="Nathaniel", font=attfont,command=name4Push)
        it4.grid(row=1, column=3)

        img5 = tk.Button(leftFrame,image=render5,command=p5Push)
        img5.image = render5
        img5.grid(row=5, column=0, padx=5, pady=5)
        # label the picture 
        it5 = tk.Button(leftFrame, text="Nik", font=attfont,command=name5Push)
        it5.grid(row=4, column=0)

        img6 = tk.Button(leftFrame,image=render6,command=p6Push)
        img6.image = render6
        img6.grid(row=5, column=1, padx=5, pady=5)
        # label the picture 
        it6 = tk.Button(leftFrame, text="Emily", font=attfont,command=name6Push)
        it6.grid(row=4, column=1)

        img7 = tk.Button(leftFrame,image=render7,command=p7Push)
        img7.image = render7
        img7.grid(row=5, column=2, padx=5, pady=5)
        # label the picture 
        it7 = tk.Button(leftFrame, text="Sarah", font=attfont,command=name7Push)
        it7.grid(row=4, column=2)
        
        img8 = tk.Button(leftFrame,image=render8,command=p8Push)
        img8.image = render8
        img8.grid(row=5, column=3, padx=5, pady=5)
        # label the picture 
        it8 = tk.Button(leftFrame, text="Xinran", font=attfont,command=name8Push)
        it8.grid(row=4, column=3)

        spacer1 = Label(leftFrame)
        spacer1.grid(row=3)
        spacer1["text"]="   "

        spacer2 = Label(leftFrame)
        spacer2.grid(row=0)
        spacer2["text"]="   "
    

    # load and place pictures 
    loadAndPlacePics()

    ###########################################################################################################################################
    # function that gives a value if the button has been pushed
    def YesisPushed():
        #print("pushed")
        global player2_people
        global player2_attributes

        # check if the computer guessed correctly 
        if checkguess == 1:
            textbox["text"] = "The computer guessed correctly"
            textbox["font"]=qfont
            # wait a second before displaying the new question 
            main.after(1000)

        [msg, player2_people, player2_attributes] = ifYesPushed(player2_people, player2_attributes, guess)

        if msg!=0:
            # wait 0.25second before displaying the new question 
            main.after(250)
            textbox["text"]=msg
            textbox["font"]=qfont
        else:
            # wait 0.25second before displaying the new question 
            main.after(250)
            textbox["text"]="Please Select Next Attribute"
            textbox["font"]=qfont
            

    # function that gives a value if the button has been pushed
    def NoisPushed():
        #print("pushed")
        global player2_people
        global player2_attributes

        # check if the computer guessed correctly 
        if checkguess == 1:
            textbox["text"] = "The computer guessed incorrectly"
            textbox["font"]=qfont
            # wait a second before displaying the new question 
            main.after(1000)

        [msg, player2_people, player2_attributes] = ifNoPushed(player2_people, player2_attributes, guess)

        if msg!=0:
            # wait 0.25second before displaying the new question 
            main.after(250)
            textbox["text"]=msg
            textbox["font"]=qfont
        else:
            # wait 0.25second before displaying the new question 
            main.after(250)
            textbox["text"]="Please Select Next Attribute"
            textbox["font"]=qfont


    ############################################################################################################################################
    # buttons for yes and no response  
    buttonfont = tkfont.Font(family='Century Gothic', size=12, weight="bold")

    # yes button with green background and white text
    yesbutton = tk.Button(botFrame,text="Yes", height=1, width=10,bg='#099412', fg='#ffffff',font=buttonfont,command=YesisPushed)
    yesbutton.grid(row=4,column=1,padx=10,pady=15,sticky="n")

    # no button with red background and white text 
    nobutton = tk.Button(botFrame,text="No", height=1, width=10,bg='#ab0a0a', fg='#ffffff',font=buttonfont,command=NoisPushed)
    nobutton.grid(row=4,column=2,padx=10,pady=15,sticky="n")   


    ############################################################################################################################################
    # attributes list section 
    attrlabel = Label(rightFrame,width=10)

    # put on grid 
    attrlabel.grid(row=0, column=0, padx=20,sticky="s")

    # List of Attributes title 
    attrlabel["text"] = "Attributes List"
    attrlabel["font"]= attfont

    # button callbacks 
    def malePushed():
        # game has started the first time an attribute is pushed
        global gamestart
        gamestart = 1

        global player1_people
        global player2_people
        global player2_attributes

        # wait a 0.25second before displaying the message
        main.after(250)
        textbox["text"]="You have asked: Is the person a male?"
        textbox["font"]=qfont

        [msg1, msg2, player1_people, player2_attributes] = ifMale(player2_person, player1_people, player2_people, player2_attributes)
        # wait 0.25second before displaying the new question 
        main.after(250)
        textbox["text"]=msg1+'\n'+msg2
        textbox["font"]=qfont

    def smilePushed():
        # game has started the first time an attribute is pushed
        global gamestart
        gamestart = 1

        global player1_people
        global player2_people
        global player2_attributes

        # wait a 0.25second before displaying the message
        main.after(250)
        textbox["text"]="You have asked: Is the person smiling?"
        textbox["font"]=qfont

        [msg1, msg2, player1_people, player2_attributes] = ifSmiling(player2_person, player1_people, player2_people, player2_attributes)
        # wait 0.25second before displaying the new question 
        main.after(250)
        textbox["text"]=msg1+'\n'+msg2
        textbox["font"]=qfont

    def hatPushed():
        # game has started the first time an attribute is pushed
        global gamestart
        gamestart = 1

        global player1_people
        global player2_people
        global player2_attributes

        # wait a 0.25second before displaying the message
        main.after(250)
        textbox["text"]="You have asked: Is the person wearing a hat?"
        textbox["font"]=qfont

        [msg1, msg2, player1_people, player2_attributes] = ifHat(player2_person, player1_people, player2_people, player2_attributes)
        # wait 0.25second before displaying the new question 
        main.after(250)
        textbox["text"]=msg1+'\n'+msg2
        textbox["font"]=qfont

    def blondePushed():
        # game has started the first time an attribute is pushed
        global gamestart
        gamestart = 1

        global player1_people
        global player2_people
        global player2_attributes

        # wait a 0.25second before displaying the message
        main.after(250)
        textbox["text"]="You have asked: Does the person have blonde hair?"
        textbox["font"]=qfont

        [msg1, msg2, player1_people, player2_attributes] = ifBlonde(player2_person, player1_people, player2_people, player2_attributes)
        # wait 0.25second before displaying the new question 
        main.after(250)
        textbox["text"]=msg1+'\n'+msg2
        textbox["font"]=qfont

    def glassesPushed():
        # game has started the first time an attribute is pushed
        global gamestart
        gamestart = 1

        global player1_people
        global player2_people
        global player2_attributes

        # wait a 0.25second before displaying the message
        main.after(250)
        textbox["text"]="You have asked: Is the person wearing glasses?"
        textbox["font"]=qfont

        [msg1, msg2, player1_people, player2_attributes] = ifEyeglasses(player2_person, player1_people, player2_people, player2_attributes)
        # wait 0.25second before displaying the new question 
        main.after(250)
        textbox["text"]=msg1+'\n'+msg2
        textbox["font"]=qfont


    # attribute buttons  
    buttonfont = tkfont.Font(family='Century Gothic', size=10)

    # male button
    malebut = tk.Button(rightFrame,text="Is Male?", height=1, width=18,font=buttonfont,command=malePushed)
    malebut.grid(row=1,column=0,padx=30,pady=10,sticky="n")

    # smiling button 
    smilebut = tk.Button(rightFrame,text="Is Smiling?", height=1, width=18,font=buttonfont,command=smilePushed)
    smilebut.grid(row=2,column=0,padx=30,pady=10,sticky="n")   

    # hat button
    hatbut = tk.Button(rightFrame,text="Is Wearing a Hat?", height=1, width=18,font=buttonfont,command=hatPushed)
    hatbut.grid(row=3,column=0,padx=30,pady=10,sticky="n")

    # blond hair button 
    blondebut = tk.Button(rightFrame,text="Has Blonde Hair?", height=1, width=18,font=buttonfont,command=blondePushed)
    blondebut.grid(row=4,column=0,padx=30,pady=10,sticky="n")  

    # glasses button 
    glassesbut = tk.Button(rightFrame,text="Is Wearing Glasses?", height=1, width=18,font=buttonfont,command=glassesPushed)
    glassesbut.grid(row=5,column=0,padx=30,pady=10,sticky="n")  

win1()
main.mainloop()

