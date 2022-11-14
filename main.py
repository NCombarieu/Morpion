#!/usr/bin/python3     

from grid import *
import random, socket, select

#creer socket d'écoute
ss = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port = 7777
ss.bind(('', port))
ss.listen(2)

players=[]

#tant qu'il n'y a pas 2 joueurs
while len(players) < 2:
    #on attend une connexion
    readl, _, _ = select.select(players+[ss], [], [])
    for s in readl:
        #si c'est la socket d'écoute, on accepte la connexion
        if s == ss:
            #nouveau joueur
            sc, addr = s.accept()
            #Ajouter le joueur à la liste
            players.append(sc)
            print("Connection from : ", sc.getpeername())

            for p in players:
                if p != sc:
                    #envoyer le nouveau joueur à tous les autres joueurs déjà connectés
                    p.sendall(b"Connected")

#Lancement du jeu
grids = [grid(), grid(), grid()]
#for p in players:
    #envoyer la grille à chaque joueur
#    p.sendall(grids[0].serialize())

#le joueur 1 commence
current_player = J1
#tant qu'il n'y a pas de gagnant
while grids[0].gameOver() == -1:
    #si c'est le tour du joueur 1
    if current_player == J1:
        shot = -1
        #tant que le joueur 1 n'a pas tiré sur une case valide
        while shot <0 or shot >=NB_CELLS:
            shot = int(input ("quel case allez-vous jouer ?"))
        
    #si c'est le tour du joueur 2
    else:
        shot = -1
        #tant que le joueur 2 n'a pas tiré sur une case valide
        while shot <0 or shot >=NB_CELLS:
            shot = int(input ("quel case allez-vous jouer ?"))
    #si la case est déjà occupée
    if (grids[0].cells[shot] != EMPTY):
        #le tour est perdu
        grids[current_player].cells[shot] = grids[0].cells[shot]
    else:
        #sinon, on joue la case
        grids[current_player].cells[shot] = current_player
        grids[0].play(current_player, shot)
        #on change de joueur
        current_player = current_player%2+1

print("game over")
#on envoie la grille à tous les joueurs

for p in players:
    p.sendall(str(grids[0].display()).encode("utf-8"))

#if grids[0].gameOver() == J1:
#    print("Tu as gagné !")
#else:
#    print("Tu as perdu !")
