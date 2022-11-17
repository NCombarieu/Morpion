#!/usr/bin/python3     

from grid import *
import socket, select, threading

class ThreadForClient(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.player = 0
        self.game = grid()

    def run(self):
        print("New thread for client " + str(self.addr))
        self.conn.send(b"Welcome to the server")
        while True:
            data = self.conn.recv(1024)
            if not data:
                print("Connection closed by client")
                break
            print("DATA : " + data.decode("utf-8"))
            self.conn.send(b"DATA : " + data)
        self.conn.close()

#------------------------------------------------------------


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
                sc.send(b"Welcome to the game !")

                for p in players:
                    if p != ss:
                        #envoyer le nouveau joueur à tous les autres joueurs déjà connectés
                        sc.send(b"Player connected")
    
    #on a 2 joueurs, on peut commencer la partie
    grids = [grid(), grid(), grid()]
    
    #socket 1 = joueur 1
    #socket 2 = joueur 2


    #on envoie les grilles aux joueurs
    for i in range(2):
        players[i].send(b"Grids")
        players[i].send(grids[i+1].display().encode("utf-8"))

    #on envoie le joueur qui commence
    players[0].send(b"Start")
    players[1].send(b"Wait")

    #tant qu'il n'y a pas de gagnant
    while grids[0].gameOver() == -1:
        #on attend un message du joueur 1
        readl, _, _ = select.select(players, [], [])
        for s in readl:
            #si c'est le joueur 1
            if s == players[0]:
                current_player = J1
                #on attend le message
                data = s.recv(1024)
                #on récupère la case jouée
                shot = int(data.decode("utf-8"))
                #on joue la case
                grids[1].play(current_player, shot)
                #on affiche la grille
                grids[0].display()
                #on envoie la grille au joueur 1
                players[0].send(b"Grids")
                players[0].send(grids[0].toBytes())
                players[0].send(grids[1].toBytes())
                #on envoie au joueur 1 qu'il doit attendre
                players[0].send(b"Wait")
                #on envoie au joueur 2 qu'il doit jouer
                players[1].send(b"Start")
            #si c'est le joueur 2
            if s == players[1]:
                current_player = J2
                #on attend le message
                data = s.recv(1024)
                #on récupère la case jouée
                shot = int(data.decode("utf-8"))
                #on joue la case
                grids[2].play(shot)
                #on envoie la grille au joueur 1
                players[0].send(b"Grids")
                players[0].send(grids[1].toBytes())
                players[0].send(grids[0].toBytes())
                #on envoie au joueur 2 qu'il doit attendre
                players[1].send(b"Wait")
                #on envoie au joueur 1 qu'il doit jouer
                players[0].send(b"Start")


            
        #si c'est le tour du joueur 1
        #if current_player == J1:
        #    shot = -1
        #    #tant que le joueur 1 n'a pas tiré sur une case valide
        #    while shot <0 or shot >=NB_CELLS:
        #        players[current_player].send(b"Your turn")
        #        shot = sc.recv(1500)
        #        shot = int(shot.decode("utf-8"))
        #        print("shot : "+ shot)
        #        shot = int(input ("quel case allez-vous jouer ? " + str(current_player)))            
        #si c'est le tour du joueur 2
        #else:
        #    shot = -1
        #    #tant que le joueur 2 n'a pas tiré sur une case valide
        #    while shot <0 or shot >=NB_CELLS:
        #        print("shot : "+ shot)
        #        shot = int(input ("quel case allez-vous jouer ? " + str(current_player)))
        #si la case est déjà occupée
        #if (grids[0].cells[shot] != EMPTY):
        #    #le tour est perdu
        #    grids[current_player].cells[shot] = grids[0].cells[shot]
        #else:
        #    #sinon, on joue la case
        #    grids[current_player].cells[shot] = current_player
        #    grids[0].play(current_player, shot)
        #    #on change de joueur
        #    current_player = current_player%2+1

    print("game over")
    #on envoie la grille en socket aux clients
    for p in players:
        print(str(p.getpeername()))
        players[p].send(str(grids[0].display()).encode("utf-8"))
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


