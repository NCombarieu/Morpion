# coding: utf-8
#!/usr/bin/env python3

import socket
import time

def send():
    dataReceivedByTheServer = input("Enter a number between 0 et 8: ")
    if 0 <= int(dataReceivedByTheServer) <= 8:
        socket.send(dataReceivedByTheServer.encode())
    else:
        send()


# define host and port
host = "localhost"
port = 15555

# create socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to server
socket.connect((host, port))
print("Connection on {}".format(port))

# receive data from server
data = socket.recv(255)
print(data)

# send data to server
  # tant que data est differen de you loose ou you win
while data != b'0' and data != b'1':
    data = socket.recv(255)
    print(data)
    if data != b'0' and data != b'1':
        send()
if data == b'0':
    print("You win")
if data == b'1':
    print("You loose")

# close socket
print("Close")
socket.close()