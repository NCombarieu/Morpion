#!/usr/bin/env python3

import socket, sys
from common import *

# define host and port
if len(sys.argv) != 3:
    print("Usage : python3 client.py host (localhost) port (50000)")
    exit()
else:
    host = sys.argv[1]
    port = int(sys.argv[2])

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to server
s.connect((host, port))

while True:
    """ Receive the message from the server """
    # receive action from server
    action = s.recv(1)
    # Si le serveur est fermé, on quitte
    if action == b"":
        break
    # decode action
    action = int(action.decode())

    if action == SHOW_GRID:
        grid = s.recv(98).decode()
        print(grid)
    elif action == GET_CLIENT_SHOT:
        s.send(input("Quelle case voulez-vous jouer ?").encode("utf-8"))
    elif action == WINNER:
        print("You WIN !")
    elif action == LOOSER:
        print("You Loose noob !")
    elif action == REPLAY:
        s.send(input("Voulez-vous rejouer ? (Y / N)\n").encode("utf-8"))

# close socket
print("Close")
s.close()