#!/usr/bin/env python3

import socket, select
from grid import *
from constants import *

############################################################################################################

def new_client(sc):
    """ Add a new client to the list """
    clients.append(sc)
    print("Nouvelle connexion !")
    if len(clients) == 2:
        print("Deux joueurs connectés, on peut commencer la partie !")
        start_game()
    elif len(clients) > 2:
        print("Un spectateur vient de se connecter !")
        sc.send(str(SPECTATOR).encode())
    else:
        print("En attente d'un autre joueur...")
        sc.send(str(WAITING).encode())
        
     
def player_shot(current_player):
    """ Ask the player to play and return the case number """
    sc = clients[current_player-1]
    shot = -1
    while shot <0 or shot >=NB_CELLS:
        sc.send(str(GET_CLIENT_SHOT).encode())
        shot = int(sc.recv(1024).decode())
    return shot

def player_send_grid(current_player, grid):
    """ Send the grid to the player """
    sc = clients[current_player-1]
    sc.send(str(SHOW_GRID).encode())
    sc.send(grid.sendDisplay().encode())

def send_win_to_player(current_player):
    """ Send the win message to the player """
    sc = clients[current_player-1]
    sc.send(str(WINNER).encode())

def send_loose_to_player(current_player):
    """ Send the loose message to the player """
    sc = clients[current_player-1]
    sc.send(str(LOOSER).encode())

def send_score(current_player, Score):
    """ Send the score to the players """
    sc = clients[current_player-1]
    sc.send(str(SCORE).encode())
    score = "Score : J1 = " + str(Score[J1-1]) + " J2 = " + str(Score[J2-1]) + "\n"
    sc.send(score.encode())

def request_replay():
    """ Ask the players if they want to replay """
    for player in [J1, J2]:
        sc = clients[player-1]
        sc.send(str(REPLAY).encode())
        if sc.recv(1).decode() != "Y":
            return False
    return True
        
############################################################################

# Create a TCP/IP socket
try:
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
except socket.error as msg:
    print("Erreur de création de la socket : " + str(msg))
    exit()

HOST = 'localhost'
PORT = 50000

# Bind the socket to the port
try:
    ss.bind((HOST, PORT))
    ss.listen(2)
except socket.error as msg:
    print("Erreur de bind ou de listen : " + str(msg))
    exit()

# Define a list to store the clients sockets
clients = []

print("Serveur en attente de connexion ...")
while len(clients) < 2:
    """ Wait for 2 clients """
    readl, _, _ = select.select(clients+[ss], [], [])
    for s in readl:
        if s is ss:
            client, addr = s.accept()
            clients.append(client)
            print("Client connecté : " + str(addr))
            s.send(str(NEW_PLAYER).encode())

############################################################################

rejouer = True
score = [0, 0]

while rejouer:
    """Main loop"""
    grids = [grid(), grid(), grid()]
    current_player = J1
    send_score(current_player, score)
    while grids[0].gameOver() == -1:
        """ Game loop """
        player_send_grid(current_player, grids[current_player])
        shot = player_shot(current_player)
        if (grids[0].cells[shot] != EMPTY):
            grids[current_player].cells[shot] = grids[0].cells[shot]
            player_send_grid(current_player, grids[current_player])
        else:
            grids[current_player].cells[shot] = current_player
            grids[0].play(current_player, shot)
            player_send_grid(current_player, grids[current_player])
            current_player = current_player%2+1
        
        print("Grille 0\n")
        grids[0].display()

    for player in [J1, J2]:
        if grids[0].gameOver() == player:
            score[player-1] += 1
            send_win_to_player(player)
        else:
            send_loose_to_player(player)

    #rejouer = False
    rejouer = request_replay()
            

print("Partie terminée, les joueurs ne veulent pas rejouer\n")

# fermer les socket clients
print("Fermeture des sockets clients")
for client in clients:
    client.close()

ss.close()