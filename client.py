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