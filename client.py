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
PLAYER_NAME = None
NAME_ENTRY = None
NAME_WINDOW = None

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
    bg = ImageTk.PhotoImage(file='./assets/background.png')
    CANVAS1 = Canvas(NAME_WINDOW,width=500,height=500)
    CANVAS1.pack(fill='both',expand=True)
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

setup()
askPlayerName()