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
continuer = 1

while continuer == 1:
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
                        p.sendall(b"J2 Connected")
    
    #on a 2 joueurs, on peut commencer la partie
    grids = [grid(), grid(), grid()]
    #le joueur 1 commence
    current_player = J1
    #tant qu'il n'y a pas de gagnant
    while grids[0].gameOver() == -1:
        #si c'est le tour du joueur 1
        if current_player == J1:
            shot = -1
            #tant que le joueur 1 n'a pas tiré sur une case valide
            while shot <0 or shot >=NB_CELLS:
                shot = int(input ("quel case allez-vous jouer ? " + str(current_player)))            
        #si c'est le tour du joueur 2
        else:
            shot = -1
            #tant que le joueur 2 n'a pas tiré sur une case valide
            while shot <0 or shot >=NB_CELLS:
                shot = int(input ("quel case allez-vous jouer ? " + str(current_player)))
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
    #on envoie la grille en socket aux clients
    for p in players:
        print(str(p.getpeername()))
        p.sendall(str(grids[0].display()).encode("utf-8"))
    #on attend que les 2 joueurs aient quitté la partie
    while len(players) > 0:
        readl, _, _ = select.select(players, [], [])
        for s in readl:
            #si un joueur quitte la partie
            if s.recv(1024) == b"":
                #on le supprime de la liste
                players.remove(s)
                print("Connection closed : ", s.getpeername())
                break

    #on recommence une nouvelle partie
    continuer = int(input("Nouvelle partie ? 1:oui 2:non"))
    print(continuer)
    print("---------------------")
    print("-------NEW GAME------")
    print("---------------------")



#fermer la socket d'écoute
ss.close()


