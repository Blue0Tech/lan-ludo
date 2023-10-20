import socket
from threading import Thread

SERVER = None
PORT = None
IP_ADDRESS = None

clients = {}

def setup():
    print("\n")
    print("\t\t\t\t\t\t\t*** LUDO LADDER ****")
    global SERVER
    global PORT
    global IP_ADDRESS
    IP_ADDRESS = '127.0.0.1'
    PORT = 5000
    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS,PORT))
    SERVER.listen(10)
    print('\n\t\t\t\t\t\t\tWaiting for connections')
    print("\n")
    accept_connections()

def accept_connections():
    global SERVER
    global clients

    while(True):
        player_socket, address = SERVER.accept()
        player_name = player_socket.recv(1024).decode('utf-8').strip()   
        if(len(clients.keys())==0):
            clients[player_name] = {'player_type':'player1'}
        else:
            clients[player_name] = {'player_type':'player2'}
        clients[player_name]['player_socket'] = player_socket
        clients[player_name]['address'] = address
        clients[player_name]['turn'] = False
        clients[player_name]['player_name'] = player_name
        print('Connection established with '+player_name+': '+address[0])

setup()