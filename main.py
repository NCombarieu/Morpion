#!/usr/bin/python3
import socket, select
from grid import *
import  random

def main():
    ss = socket.socket(socket.AF_INET ,socket.SOCK_STREAM, 0)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = "127.0.0.1"
    port = 7777
    ss.bind((host, port))
    ss.listen(1)

    #initialisation d'une liste pour les sockets clientes
    l = []
    joueur = True

    while True:
        #j'ajoute la socket server a ma liste
        readl, _, _ = select.select(l+[ss],[],[])

        #Pour chaque socket présente dans la liste de socket : 
        for s in readl:
            if s == ss :
                sc, a = s.accept()
                l.append(sc)
                print("new client :" ,a)
                if l.count(sc)>1:
                    False
            
            else:    
                msg = s.recv(1500)
                #Si le message recu est nul, le client est déconnecté puis on supprime le socket de la liste
                if len(msg) == 0:
                    print (" client disconnected ")
                    peername = sc.getpeername()
                    newClient = "Client disconnected :" + str(peername)+ " : " + str(port) +"\n"
                    for s2 in l:
                        s2.sendall(newClient.encode("utf-8"))
                    s.close()
                    l.remove(s)
        
    
    print(l.count(sc))

    grids = [grid(), grid(), grid()]
    current_player = J1
    
    grids[J1].display()
    while grids[0].gameOver() == -1:
        if current_player == J1:
            shot = -1
            while shot <0 or shot >=NB_CELLS:
                shot = int(input ("quel case allez-vous jouer ?"))
        else:
            shot = random.randint(0,8)
            while grids[current_player].cells[shot] != EMPTY:
                shot = random.randint(0,8)
        if (grids[0].cells[shot] != EMPTY):
            grids[current_player].cells[shot] = grids[0].cells[shot]
        else:
            grids[current_player].cells[shot] = current_player
            grids[0].play(current_player, shot)
            current_player = current_player%2+1
        if current_player == J1:
            grids[J1].display()
    print("game over")
    grids[0].display()
    if grids[0].gameOver() == J1:
        print("You win !")
    else:
        print("you loose !")

main()
