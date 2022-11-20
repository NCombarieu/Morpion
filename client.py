<<<<<<< HEAD
#!/usr/bin/env python3

import socket, sys
from constants import *

# define host and port
if len(sys.argv) != 3:
    print("Usage : python3 client.py <host> <port>")
    exit()
else:
    host = sys.argv[1]
    port = int(sys.argv[2])

# create socket
try:
    sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sc.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
except socket.error as msg:
    print("Erreur de création de la socket : " + str(msg))
    exit()
# connect to server
try:
    sc.connect((host, port))
except socket.error as msg:
    print("Erreur de connexion : " + str(msg))
    exit()

while True:
    """ Receive the message from the server """
    # receive action from server
    action = sc.recv(1)
    # if action is empty, the server has closed the connection
    if action == b"":
        break
    # parse action to int and execute the corresponding action
    action = int(action.decode())

    if action == SHOW_GRID:
        grid = sc.recv(98).decode()
        print(grid)
    elif action == GET_CLIENT_SHOT:
        sc.send(input("Quelle case voulez-vous jouer ?").encode("utf-8"))
    elif action == WINNER:
        print("You WIN !")
    elif action == LOOSER:
        print("You Loose noob !")
    elif action == SCORE:
        score = sc.recv(22).decode()
        print(score)
    elif action == REPLAY:
        sc.send(input("Voulez-vous rejouer ? (Y / N)\n").encode("utf-8"))

# close socket
print("Close")
sc.close()
=======
#client du serveur pour le morpion
import socket
import select
import sys
import os

# Constantes
HOST = 'localhost'
PORT = 50000

# Fonctions
def initSocket():
    # Création de la socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print("Erreur de création de la socket : " + str(msg))
        exit()
    print("Socket créée")

    # On se connecte au serveur
    try:
        s.connect((HOST, PORT))
    except socket.error as msg:
        print("Erreur de connexion : " + str(msg))
        exit()
    print("Connexion établie avec le serveur")

    return s

def initGame(s):
    # On attend le début de la partie
    print("En attente du début de la partie")
    while True:
        readl, _, _ = select.select([s], [], [])
        for s in readl:
            msg = s.recv(1024).decode("utf-8")
            print(msg)
            if msg == "Début de la partie":
                break
    print("Début de la partie")

def play(s):
    # On joue
    print("C'est à vous de jouer")
    while True:
        readl, _, _ = select.select([s], [], [])
        for s in readl:
            msg = s.recv(1024).decode("utf-8")
            print(msg)
            if msg == "Fin de la partie":
                break
    print("Fin de la partie")

def main():
    # On initialise la socket
    s = initSocket()

    # On initialise la partie
    initGame(s)

    # On joue
    play(s)

    # On ferme la socket
    s.close()
>>>>>>> master
