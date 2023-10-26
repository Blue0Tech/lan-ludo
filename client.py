import socket
from threading import Thread
from tkinter import *
from PIL import ImageTk, Image
import random

SERVER = None
PORT = None
IP_ADDRESS = None
SCREEN_WIDTH = None
SCREEN_HEIGHT = None
CANVAS1 = None
CANVAS2 = None
PLAYER_NAME = None
NAME_ENTRY = None
NAME_WINDOW = None
GAME_WINDOW = None
DICE = None
LEFT_BOXES = []
RIGHT_BOXES = []
FINISHING_BOX = None
PLAYER_TYPE = None
PLAYER_TURN = None
ROLL_BUTTON = None

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS
    PORT = 5000
    IP_ADDRESS = '127.0.0.1'
    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS,PORT))

def askPlayerName():
    global PLAYER_NAME
    global NAME_ENTRY
    global NAME_WINDOW
    global SCREEN_HEIGHT
    global SCREEN_WIDTH
    global CANVAS1

    NAME_WINDOW = Tk()
    NAME_WINDOW.title('LUDO LADDER')
    NAME_WINDOW.attributes('-fullscreen',True)
    SCREEN_WIDTH = NAME_WINDOW.winfo_screenwidth()
    SCREEN_HEIGHT = NAME_WINDOW.winfo_screenheight()
    CANVAS1 = Canvas(NAME_WINDOW,width=500,height=500)
    CANVAS1.pack(fill='both',expand=True)
    bg = ImageTk.PhotoImage(master=CANVAS1,file='./assets/background.png')
    CANVAS1.create_image(0,0,anchor='nw',image=bg)
    CANVAS1.create_text(SCREEN_WIDTH/2,SCREEN_HEIGHT/5,text='Enter name',font=("Chalkboard SE",100))
    NAME_ENTRY = Entry(NAME_WINDOW,width=15,justify='center',font=('Chalkboard SE', 50), bd=5, bg='white')
    NAME_ENTRY.place(x=(SCREEN_WIDTH/2)-230,y=(SCREEN_HEIGHT/4)+100)
    button = Button(NAME_WINDOW,text='Save',font=('Helvetica',30),width=15, command=saveName,height=2,bg='grey')
    button.place(x=(SCREEN_WIDTH/2)-130,y=(SCREEN_HEIGHT/2))
    NAME_WINDOW.mainloop()

def saveName():
    global PLAYER_NAME
    global NAME_WINDOW
    global NAME_ENTRY
    global SERVER
    PLAYER_NAME = NAME_ENTRY.get()
    NAME_ENTRY.delete(0,END)
    NAME_WINDOW.destroy()
    SERVER.send(PLAYER_NAME.encode('utf-8'))
    gameWindow()

def gameWindow():
    global GAME_WINDOW
    global CANVAS2
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global DICE

    GAME_WINDOW = Tk()
    GAME_WINDOW.title('LUDO LADDER')
    GAME_WINDOW.attributes('-fullscreen',True)
    SCREEN_WIDTH = GAME_WINDOW.winfo_screenwidth()
    SCREEN_HEIGHT = GAME_WINDOW.winfo_screenheight()
    
    CANVAS2 = Canvas(GAME_WINDOW,width=500,height=500)
    CANVAS2.pack(fill='both',expand=True)
    bg = ImageTk.PhotoImage(master=CANVAS2,file='./assets/background.png')
    CANVAS2.create_image(0,0,image=bg,anchor='nw')
    CANVAS2.create_text(SCREEN_WIDTH/2,SCREEN_HEIGHT/5,text='LUDO LADDER',font=('Chalkboard SE',100),fill='white')
    
    leftBoard()
    rightBoard()
    finishingBox()
    createRollButton()

    # start thread of receiving messages where if it's player turn then call createRollButton again

    GAME_WINDOW.resizable(True,True)
    GAME_WINDOW.mainloop()

def receiveMessages():
    global SERVER

    while(True):
        msg = SERVER.recv(2048).decode('utf-8')
        #

def leftBoard():
    global GAME_WINDOW
    global LEFT_BOXES
    global SCREEN_HEIGHT

    xpos = 116
    for box in range(0,11):
        if(box==0):
            boxLabel = Label(GAME_WINDOW,font=('Helvetica',30),width=2,height=1,relief=RIDGE,borderwidth=0,bg='red')
            boxLabel.place(x=xpos,y=SCREEN_HEIGHT/2-88)
            LEFT_BOXES.append(boxLabel)
        else:
            boxLabel = Label(GAME_WINDOW,font=('Helvetica',30),width=2,height=1,relief=RIDGE,borderwidth=0,bg='white')
            boxLabel.place(x=xpos,y=SCREEN_HEIGHT/2-100)
            LEFT_BOXES.append(boxLabel)
        xpos += 50

def rightBoard():
    global GAME_WINDOW
    global RIGHT_BOXES
    global SCREEN_HEIGHT

    xpos = 858
    for box in range(0,11):
        if(box==10):
            boxLabel = Label(GAME_WINDOW,font=('Helvetica',30),width=2,height=1,relief=RIDGE,borderwidth=0,bg='yellow')
            boxLabel.place(x=xpos,y=SCREEN_HEIGHT/2-88)
            RIGHT_BOXES.append(boxLabel)
        else:
            boxLabel = Label(GAME_WINDOW,font=('Helvetica',30),width=2,height=1,relief=RIDGE,borderwidth=0,bg='white')
            boxLabel.place(x=xpos,y=SCREEN_HEIGHT/2-100)
            RIGHT_BOXES.append(boxLabel)
        xpos += 50

def finishingBox():
    global GAME_WINDOW
    global FINISHING_BOX
    global SCREEN_WIDTH
    global SCREEN_HEIGHT

    finishing_box = Label(GAME_WINDOW,text='HOME',font=('Chalkboard SE',32),width=8,height=4,borderwidth=0,bg='green',fg='white')
    finishing_box.place(x=SCREEN_WIDTH/2-108,y=SCREEN_HEIGHT/2-160)

def rollDice():
    global CANVAS2
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global PLAYER_TYPE
    global PLAYER_TURN
    global ROLL_BUTTON
    global SERVER

    dice = CANVAS2.create_text(SCREEN_WIDTH/2+10,SCREEN_HEIGHT/2+250,text='\u2680',font=('Chalkboard SE',250),fill='white')
    dice_choices = ['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']

    value = random.choice(dice_choices)
    ROLL_BUTTON.destroy()
    PLAYER_TURN = False
    if(PLAYER_TYPE=='player1'):
        SERVER.send(f'{value} player2turn'.encode("utf-8"))
    if(PLAYER_TYPE=='player2'):
        SERVER.send(f'{value} player1turn'.encode("utf-8"))
    dice.__setattr__('-text',value)

def createRollButton():
    global GAME_WINDOW
    global SCREEN_HEIGHT
    global SCREEN_WIDTH
    global ROLL_BUTTON

    ROLL_BUTTON = Button(GAME_WINDOW,text='ROLL DICE',fg='black',font=('Chalkboard SE',15),bg='grey',command=rollDice,width=20,height=5)
    ROLL_BUTTON.place(x=SCREEN_WIDTH/2-10,y=SCREEN_HEIGHT/2+50)


setup()
askPlayerName()