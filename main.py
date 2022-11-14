#!/usr/bin/env python3
from grid import *
import socket, select, pickle, sys
import  random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt (socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
s.bind(('localhost', 7777))
s.listen(2)

players=[]
    
while True:
    while len(players) < 2:
        listL, _, _ = select.select(players+[s],[],[])
        for ss in listL:
            if s==ss:
                sc , a = s.accept ()
                print("{} connected".format(a))
                sc.sendall(pickle.dumps([players[ss],len(players)]))	
                players.append(sc)

    grids = [grid(), grid(), grid()]
    current_player = J1
    grids[J1].display()

    while grids[0].gameOver() == -1:
        if current_player == J1:
            shot = -1
            while shot < 0 or shot >= NB_CELLS:
                data = "ok"
                client.send(data.encode())
                shot = int(client.recv(255))
        else:
            current_player = J2

            shot = int(client.recv(255))
            while grids[current_player].cells[shot] != EMPTY:
                shot = random.randint(0, 8)
        if (grids[0].cells[shot] != EMPTY):
            grids[current_player].cells[shot] = grids[0].cells[shot]
        else:
            grids[current_player].cells[shot] = current_player
            grids[0].play(current_player, shot)
            current_player = current_player % 2 + 1
        if current_player == J1:
            grids[J1].display()
    grids[0].display()
    if grids[0].gameOver() == J1:
        data = "0"
    else:
        data = "1"
    client.send(data.encode())
# client.close()