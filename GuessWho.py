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
mframe.pack() #row=0,column=0)


pushed = 0

# Clear the main windows frame of all widgets
def clearwin(event=None):
    for child in mframe.winfo_children():
        child.destroy()
    mframe.pack_forget()
    mframe.grid_forget

def win1(event=None):
    '''Create the main window'''
    clearwin()

    # define title font style 
    title_font = tkfont.Font(family='Helvetica', size=30, weight="bold")

    # define text at top of page 
    label = tk.Label(text="Guess Who?", font=title_font)
    label.pack(side="top", fill="x", pady=10)

    # add game instructions 
    # font
    instructFont = tkfont.Font(family='Helvetica', size=12)
    instructtext = "Instructions on how to play the game once we decide on those.. blah blah blah more stuff"
    instructtext = instructtext + " and more and more and more"
    instructlabel = tk.Label(text=instructtext,font=instructFont)
    instructlabel.pack(pady=10)

    # button to start the game, green background with white words 
    # buton font 
    buttonfont = tkfont.Font(family='Helvetica', size=12, weight="bold")
    button = tk.Button(text="Begin Game", height=2, width=15,bg='#099412', fg='#ffffff',
        command=win2,font=buttonfont)
    button.pack(pady=10)

    # add project and creators label 
    botFont = tkfont.Font(family='Helvetica', size=11)
    creatrlabel = tk.Label(text="Xinran Li, Lin Liu, Nathaniel Nyberg, Sarah Ziselman",font=botFont)
    creatrlabel.pack(pady=15)
    projlabel = tk.Label(text="ELEC_ENG_475: Machine Learning: Foundations, Applications, and Algorithms Final Project",font=botFont)
    projlabel.pack()




def win2():
    '''Create the second sub window'''
    clearwin()

    # define font style 
    title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

    # load and place pictures 
    loadAndPlacePics()

    # text box where the computer will communicate with the player, scrolls so older messages will be higher up 
    textbox = Label(height=10,width=30)

    # put on grid 
    textbox.grid(row=3, column=0,columnspan=2)
    
    #pushed = 0
    # function that gives a value if the button has been pushed
    def YesisPushed(pushed):
        print("pushed")
        #global pushed
        msg = "Does your person have"
        textbox["text"]=msg
        pushed=1
        

    # function that gives a value if the button has been pushed
    def NoisPushed(pushed):
        print("pushed")
        #global pushed
        msg = "No"
        textbox["text"]=msg
        pushed=1
        

    

    # buttons for yes and no response  
    buttonfont = tkfont.Font(family='Helvetica', size=12, weight="bold")

    # yes button with green background and white text
    yesbutton = tk.Button(main,text="Yes", height=1, width=10,bg='#099412', fg='#ffffff',font=buttonfont,command=lambda *args:YesisPushed(pushed))
    yesbutton.grid(row=4,column=1,padx=10,pady=15,sticky="n")

    # no button with red background and white text 
    nobutton = tk.Button(main,text="No", height=1, width=10,bg='#ab0a0a', fg='#ffffff',font=buttonfont,command=lambda *args:NoisPushed(pushed))
    nobutton.grid(row=4,column=2,padx=10,pady=15,sticky="n")   

    #main.after(1000,win2)
    #main.update_idletasks()
    #main.update()
    #main.mainloop()

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
    

    # place the images on a 2x4 grid with borders along x and y to space out the pictures 
    img1 = Label(image=render1)
    img1.image = render1
    img1.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    img2 = Label(image=render2)
    img2.image = render2
    img2.grid(row=0, column=1, padx=5, pady=5)

    img3 = Label(image=render3)
    img3.image = render3
    img3.grid(row=0, column=2, padx=5, pady=5)

    img4 = Label(image=render4)
    img4.image = render4
    img4.grid(row=0, column=3, padx=5, pady=5)

    img5 = Label(image=render5)
    img5.image = render5
    img5.grid(row=1, column=0, padx=5, pady=5, sticky="e")

    img6 = Label(image=render6)
    img6.image = render6
    img6.grid(row=1, column=1, padx=5, pady=5)

    img7 = Label(image=render7)
    img7.image = render7
    img7.grid(row=1, column=2, padx=5, pady=5)
    
    img8 = Label(image=render8)
    img8.image = render8
    img8.grid(row=1, column=3, padx=5, pady=5)
    


        

        #button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("StartPage"))
        #button.pack()

# test class with functions related to the computer player 
class Test():
    def getMessage(): 
        return "hi"
    


gameInProgress = True
win2()
main.mainloop()

#while gameInProgress:
#    win2()
    #while True:
        #win2()
        #main.update_idletasks()
    #    main.update()
    #main.mainloop()

'''
class GameWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # name the window 
        self.title("Guess Who Game")

        # make window not resizable
        self.resizable(width=False, height=False)

        # use container to stack a bunch of frames on top of each other
        container = tk.Frame(self)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # organize widgets in blocks
        container.pack(side="top", fill="both", expand=True)

        # stack frames on top of each other 
        self.frames = {}
        for F in (StartPage, GamePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location
            # frame on top of stack will be visible.
            frame.grid(row=0, column=0, sticky="nsew")
        # all frames have been stacked

        self.show_frame("StartPage")

    # function to show the frame with the page_name
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # define title font style 
        self.title_font = tkfont.Font(family='Helvetica', size=30, weight="bold")

        # define text at top of page 
        label = tk.Label(self, text="Guess Who?", font=self.title_font)
        label.pack(side="top", fill="x", pady=10)

        # add game instructions 
        # font
        instructFont = tkfont.Font(family='Helvetica', size=12)
        instructtext = "Instructions on how to play the game once we decide on those.. blah blah blah more stuff"
        instructtext = instructtext + " and more and more and more"
        instructlabel = tk.Label(self, text=instructtext,font=instructFont)
        instructlabel.pack(pady=10)

        # button to start the game, green background with white words 
        # buton font 
        buttonfont = tkfont.Font(family='Helvetica', size=12, weight="bold")
        button = tk.Button(self, text="Begin Game", height=2, width=15,bg='#099412', fg='#ffffff',
            command=lambda: controller.show_frame("GamePage"),font=buttonfont)
        button.pack(pady=10)

        # add project and creators label 
        botFont = tkfont.Font(family='Helvetica', size=11)
        creatrlabel = tk.Label(self,text="Xinran Li, Lin Liu, Nathaniel Nyberg, Sarah Ziselman",font=botFont)
        creatrlabel.pack(pady=15)
        projlabel = tk.Label(self, text="ELEC_ENG_475: Machine Learning: Foundations, Applications, and Algorithms Final Project",font=botFont)
        projlabel.pack()


class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # define font style 
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        #label = tk.Label(self, text="This is page 1", font=self.title_font)
        #label.pack(side="top", fill="x", pady=10)

        # load and place pictures 
        self.loadAndPlacePics()

        # text box where the computer will communicate with the player
        # text box scrolls so older messages will be higher up 
        textbox = tk.Text(self,height=30,width=30)
        
        # put on grid 
        textbox.grid(row=0, rowspan=2, column=5,columnspan=2,padx=15)

        # buttons for yes and no response  
        # buton font 
        buttonfont = tkfont.Font(family='Helvetica', size=12, weight="bold")
        global pushed
        pushed = 0 
        test = 0
        
        # function that gives a value if the button has been pushed
        def isPushed():
            pushed=1

        # yes button with green background and white text
        yesbutton = tk.Button(self, text="Yes", height=1, width=10,bg='#099412', fg='#ffffff',font=buttonfont,command=lambda:isPushed())
        yesbutton.grid(row=3,column=5,padx=10,pady=15,sticky="n")

        # no button with red background and white text 
        nobutton = tk.Button(self, text="No", height=1, width=10,bg='#ab0a0a', fg='#ffffff',font=buttonfont,command=lambda:isPushed())
        nobutton.grid(row=3,column=6,padx=10,pady=15,sticky="n")

        
        
        # run for however long the game runs
        #while test==0:
        # textbox
        # get the message from the computer player
    
        msg = Test.getMessage()
        # allow the textbox to be edited
        textbox['state'] = 'normal'
        # insert the message at the end of the line and then insert a new line 
        textbox.insert(tk.END,msg+'\n')
        # disable textbox so the player can't write on it 
        #textbox['state'] = 'disabled'

        # buttons 
        if pushed==1: 
            msg = "good" + '\n'
            textbox.insert(tk.END,msg+'\n')
            pushed=0
            test = 10

        # disable textbox so the player can't write on it 
        textbox['state'] = 'disabled'



    # function to load the pictures and place them in a 2x4 grid
    def loadAndPlacePics(self): 
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
        

        # place the images on a 2x4 grid with borders along x and y to space out the pictures 
        img1 = Label(self,image=render1)
        img1.image = render1
        img1.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        img2 = Label(self,image=render2)
        img2.image = render2
        img2.grid(row=0, column=1, padx=5, pady=5)

        img3 = Label(self,image=render3)
        img3.image = render3
        img3.grid(row=0, column=2, padx=5, pady=5)

        img4 = Label(self,image=render4)
        img4.image = render4
        img4.grid(row=0, column=3, padx=5, pady=5)

        img5 = Label(self,image=render5)
        img5.image = render5
        img5.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        img6 = Label(self,image=render6)
        img6.image = render6
        img6.grid(row=1, column=1, padx=5, pady=5)

        img7 = Label(self,image=render7)
        img7.image = render7
        img7.grid(row=1, column=2, padx=5, pady=5)
        
        img8 = Label(self,image=render8)
        img8.image = render8
        img8.grid(row=1, column=3, padx=5, pady=5)
        


        

        #button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("StartPage"))
        #button.pack()


# test class with functions related to the computer player 
class Test():
    def getMessage(): 
        return "hi"


# main loop
if __name__ == "__main__":
    game = GameWindow()
    
    #while True:
        
    #    game.update()
    game.mainloop()


'''
'''
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
'''