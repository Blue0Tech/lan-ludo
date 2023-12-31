import socket
from threading import Thread
from tkinter import *
from PIL import ImageTk, Image
import random
import json

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
PLAYER1NAME = 'joining'
PLAYER2NAME = 'joining'
PLAYER1LABEL = None
PLAYER2LABEL = None
WINNINGFUNCTIONCALL = 0
WINNINGMESSAGE = None
RESETBUTTON = None

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
    # start thread of receiving messages where if it's player turn then call createRollButton again
    msgReceivingThread = Thread(target=receiveMessages)
    msgReceivingThread.start()
    # createRollButton()

    GAME_WINDOW.resizable(True,True)
    GAME_WINDOW.mainloop()

def receiveMessages():
    global SERVER
    global PLAYER_TYPE
    global PLAYER_NAME
    global PLAYER1NAME
    global PLAYER2NAME
    global CANVAS2
    global DICE
    global WINNINGFUNCTIONCALL

    msg = SERVER.recv(2048).decode('utf-8')
    # msg.replace('\'','"')
    info = json.loads(msg)
    PLAYER_TYPE = info['player_type']
    if(PLAYER_TYPE=='player1'):
        PLAYER1NAME = PLAYER_NAME
    else:
        PLAYER2NAME = PLAYER_NAME
    isTurn = info['turn']
    if(isTurn):
        createRollButton()
    
    while(True):
        msg = SERVER.recv(2048).decode('utf-8')
        message = msg.split(' ')
        if(PLAYER_TYPE in message[1]): # if player has not just played
            value = message[0]
            numVal = 0
            if(value == '⚀'):
                numVal = 1
            elif(value == '⚁'):
                numVal = 2
            elif(value == '⚂'):
                numVal = 3
            elif(value == '⚃'):
                numVal = 4
            elif(value == '⚄'):
                numVal = 5
            elif(value == '⚅'):
                numVal = 6
            createRollButton()
            if(PLAYER_TYPE == 'player1'):
                movePlayer2(value)
                PLAYER2NAME = message[2]
            else:
                movePlayer1(value)
                PLAYER1NAME = message[2]
        elif('wins the game!' in message and WINNINGFUNCTIONCALL == 0):
            WINNINGFUNCTIONCALL +=1
            handleWin(message)
            # updateScore(message)
        elif(message == 'reset game'):
            # handleResetGame()
            # if()
            pass

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
    global PLAYER_NAME
    global PLAYER_TURN
    global ROLL_BUTTON
    global SERVER
    global DICE

    if(DICE!=None):
        CANVAS2.delete(DICE)

    DICE = CANVAS2.create_text(SCREEN_WIDTH/2+10,SCREEN_HEIGHT/2+250,text='\u2680',font=('Chalkboard SE',250),fill='white')
    dice_choices = ['\u2680','\u2681','\u2682','\u2683','\u2684','\u2685']

    value = random.choice(dice_choices)
    numVal = 0
    if(value == '⚀'):
        numVal = 1
    elif(value == '⚁'):
        numVal = 2
    elif(value == '⚂'):
        numVal = 3
    elif(value == '⚃'):
        numVal = 4
    elif(value == '⚄'):
        numVal = 5
    elif(value == '⚅'):
        numVal = 6
    ROLL_BUTTON.destroy()
    PLAYER_TURN = False
    if(PLAYER_TYPE=='player1'):
        movePlayer1(numVal)
        SERVER.send(f'{value} player2turn {PLAYER_NAME}'.encode("utf-8"))
    if(PLAYER_TYPE=='player2'):
        movePlayer2(numVal)
        SERVER.send(f'{value} player1turn {PLAYER_NAME}'.encode("utf-8"))
    CANVAS2.itemconfig(DICE,text=value)

def createRollButton():
    global GAME_WINDOW
    global SCREEN_HEIGHT
    global SCREEN_WIDTH
    global ROLL_BUTTON

    ROLL_BUTTON = Button(GAME_WINDOW,text='ROLL DICE',fg='black',font=('Chalkboard SE',15),bg='grey',command=rollDice,width=20,height=5)
    ROLL_BUTTON.place(x=SCREEN_WIDTH/2+10,y=SCREEN_HEIGHT/2+50)

def checkColourPosition(boxes,colour):
    for box in boxes:
        box_colour = box.cget('bg')
        if(box_colour==colour):
            return boxes.index(box)
        return False

def movePlayer1(steps):
    global LEFT_BOXES
    global FINISHING_BOX
    global SERVER
    global PLAYER_NAME
    dicevalue = steps
    box_position = checkColourPosition(LEFT_BOXES[1:],'red')
    if(box_position):
        colouredBoxIndex = box_position
        totalSteps = 10
        remainingSteps = totalSteps - colouredBoxIndex
        if(steps==remainingSteps):
            for box in LEFT_BOXES[1:]:
                box.configure(bg='white')
            FINISHING_BOX.configure(bg='red')
            greetMessage = f'Red wins the game!'
            SERVER.send((greetMessage).encode('utf-8'))
        elif(steps<remainingSteps):
            for box in LEFT_BOXES[1:]:
                box.configure(bg='white')
            nextStep = (colouredBoxIndex + 1) + dicevalue
            LEFT_BOXES[nextStep].configure(bg='red')
        else:
            LEFT_BOXES[steps].configure('red')

def movePlayer2(steps):
    global RIGHT_BOXES
    global FINISHING_BOX
    global SERVER
    global PLAYER_NAME
    dicevalue = steps
    box_position = checkColourPosition(RIGHT_BOXES[-2 ::-1],'yellow')
    if(box_position):
        colouredBoxIndex = box_position
        totalSteps = 10
        remainingSteps = totalSteps - colouredBoxIndex
        if(steps==remainingSteps):
            for box in RIGHT_BOXES[-2 ::-1]:
                box.configure(bg='white')
            FINISHING_BOX.configure(bg='yellow')
            greetMessage = 'Yellow wins the game!'
            SERVER.send((greetMessage).encode('utf-8'))
        elif(steps<remainingSteps):
            for box in RIGHT_BOXES[-2 ::-1]:
                box.configure(bg='white')
            nextStep = (colouredBoxIndex + 1) + dicevalue
            RIGHT_BOXES[::1][nextStep].configure(bg='yellow')
        else:
            RIGHT_BOXES[len(RIGHT_BOXES)-steps+1].configure('yellow')

def handleWin(message):
    global PLAYER_TYPE
    global ROLL_BUTTON
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global CANVAS2
    global WINNINGMESSAGE
    global RESETBUTTON
    
    if('Red' in message):
        if(PLAYER_TYPE=='player2'):
            ROLL_BUTTON.destroy()
    elif('Yellow' in message):
        if(PLAYER_TYPE=='player1'):
            ROLL_BUTTON.destroy()
    message = message.split(' ')[0] + "."
    CANVAS2.itemconfigure(WINNINGMESSAGE,text=message)
    RESETBUTTON.place(x=SCREEN_WIDTH/2-80,y=SCREEN_HEIGHT-220)

# def receivedMessage():
#     global SERVER
#     global PLAYER_TYPE
#     global PLAYER_TURN
#     global ROLL_BUTTON
#     global SCREEN_WIDTH
#     global SCREEN_HEIGHT
#     global CANVAS2
#     global DICE
#     global GAME_WINDOW
#     global PLAYER1NAME
#     global PLAYER2NAME
#     global PLAYER1LABEL
#     global PLAYER2LABEL
#     global WINNINGFUNCTIONCALL

#     while(True):
#         message = SERVER.recv(2048).decode('utf-8')
#         if('PLAYER_TYPE' in message):
#             pass

setup()
askPlayerName()