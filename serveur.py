#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket, select
from grid import *

try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
except socket.error as msg:
    print("Erreur de création de la socket : " + str(msg))
    exit()

HOST = 'localhost'
PORT = 50000

try:
    ss.bind((HOST, PORT))
    ss.listen(2)
except socket.error as msg:
    print("Erreur de bind ou de listen : " + str(msg))
    exit()
    
clients = []
rejouer = True
score = [0, 0]

print("Serveur en attente de connexion ...")
while len(clients) < 2:
    readl, _, _ = select.select(clients+[ss], [], [])
    for s in readl:
        if s is ss:
            client, addr = s.accept()
            clients.append(client)
            print("Client connecté : " + str(addr))

for i in clients:
    if i.getpeername() == clients[0].getpeername():
        i.send("Vous êtes le joueur 1 \n".encode("utf-8"))
        i.send("Vous jouez avec les O \n".encode("utf-8"))
    elif i.getpeername() == clients[1].getpeername():
        i.send("Vous êtes le joueur 2 \n".encode("utf-8"))
        i.send("Vous jouez avec les X \n".encode("utf-8"))
    else :
        i.send("Erreur \n".encode("utf-8"))


while rejouer == True:
    # On attend la connexion des deux clients
    print("Serveur en attente de connexion ...")
    while len(clients) < 2:
        readl, _, _ = select.select(clients+[ss], [], [])
        for s in readl:
            if s is ss:
                client, addr = s.accept()
                clients.append(client)
                print("Client connecté : " + str(addr))
    
    for i in clients:
        if i.getpeername() == clients[0].getpeername():
            i.send("Vous êtes le joueur 1 \n".encode("utf-8"))
            i.send("Vous jouez avec les X \n".encode("utf-8"))
        elif i.getpeername() == clients[1].getpeername():
            i.send("Vous êtes le joueur 2 \n".encode("utf-8"))
            i.send("Vous jouez avec les O \n".encode("utf-8"))
        else :
            i.send("Erreur \n".encode("utf-8"))

    # On initialise la grille
    grids = [grid(), grid(), grid()]
    #grids[0].display()
    # On initialise le joueur
    joueur = J1
    # On initialise le tour
    tour = 0
    # On initialise la partie
    partie = True
    # On initialise le gagnant
    gagnant = 0

    while partie == True:
        # les joueurs jouent jusqu'a ce que la partie soit finie
        #gridprincipale = grids[0].display()
        #print(grid[0].display())
        while grids[0].gameOver() == -1:
            # Les joueurs jouent chaqun leur tour
            for client in clients:
                clients[0].send("C'est au tour du joueur {} \n".format(joueur).encode("utf-8"))
                clients[1].send("C'est au tour du joueur {} \n".format(joueur).encode("utf-8"))
                if client.getpeername() == clients[0].getpeername():
                    shot = -1
                    while shot <0 or shot >=NB_CELLS:
                        client.send("Quel case allez-vous jouer ? \n".encode("utf-8"))
                        shot = client.recv(1024)
                        shot = int(shot)

                    grids[0].play(joueur, shot)
                    grids[0].display()
                    grids[1].play(joueur, shot)
                    grids[2].play(joueur, shot)
                    joueur = J2
                elif client.getpeername() == clients[1].getpeername():
                    client.send("Quel case allez-vous jouer ? \n".encode("utf-8"))
                    shot = client.recv(1024)
                    shot = int(shot)
                    grids[0].play(joueur, shot)
                    grids[0].display()
                    grids[1].play(joueur, shot)
                    grids[2].play(joueur, shot)
                    joueur = J1
                else :
                    client.send("Erreur \n".encode("utf-8"))

    # On attend la réponse des clients
        partie = rejouer(clients)
        
    for client in clients:
            client.send("fin du game".encode("utf-8"))
            clients.remove(client)
            client.close()

def shot():
    shot = -1
    while shot <0 or shot >=NB_CELLS:
        shot = int(input ("quel case allez-vous jouer ?"))
    return shot

def rejouer(clients):
    for client in clients:
        client.send("Voulez-vous rejouer ?".encode("utf-8"))
        reponse = client.recv(1024)
        if reponse == "oui" or reponse == "Oui" or reponse == "OUI" or reponse == "o" or reponse == "O" or reponse == "y" or reponse == "Y":
            return True
        else:
            return False