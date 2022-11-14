#!/usr/bin/python3
import socket, sys

#create connection to server
s= socket.socket(socket.AF_INET6 , socket.SOCK_STREAM , 0)
s.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)

HOST = 'localhost'
#Si pas d'argument, on prend demande le port
if len(sys.argv) < 2:
    PORT = int(input("Port: "))
else:
    PORT = int(sys.argv[1])

s.connect((HOST, PORT))

#tant que le serveur n'a pas envoyé de message, on attend
while True:
    #On reçoit le message
    data = s.recv(1024)
    #Si le message est vide, on quitte
    if not data:
        break
    #Sinon on affiche le message
    print(data.decode("utf-8"))

#send data to server
s.sendall(b'Hello, world')
#receive data from server
data = s.recv(1024)
s.close()
