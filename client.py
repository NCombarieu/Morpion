#!/usr/bin/env python3

import socket, sys
import time

def send():
    dataReceivedByTheServer = input("Enter a number between 0 et 8: ")
    if 0 <= int(dataReceivedByTheServer) <= 8:
        socket.send(dataReceivedByTheServer.encode())
    else:
        send()


# define host and port
host = "localhost"
port = int(sys.argv[1])

# create socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to server
socket.connect((host, port))
print("Connection on {}".format(port))

# receive data from server
data = socket.recv(255)
print("1: ", data)

# send data to server
  # tant que data est differen de you loose ou you win
while data != '0' and data != '1':
    data = socket.recv(255)
    print("2 : ", data)
    if data != '0' and data != '1':
        send()
if data == b'0':
    print("You win")
if data == b'1':
    print("You loose")

# close socket
print("Close")
socket.close()