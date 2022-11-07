# coding: utf-8
#!/usr/bin/env python3
from grid import *
import socket
import  random

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(('', 15555))

while True:
    socket.listen(5)
    client, address = socket.accept()
    print("{} connected".format(address))
    data = "Hello World!"
    client.send(data.encode())

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
            shot = random.randint(0, 8)
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