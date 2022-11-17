#!/usr/bin/python3
import socket, sys

HOST = 'localhost'
#Si pas d'argument, on prend demande le port
if len(sys.argv) < 2:
    PORT = int(input("Port: "))
else:
    PORT = int(sys.argv[1])

try:
    #create connection to server
    s = socket.socket(socket.AF_INET6 , socket.SOCK_STREAM , 0)
    s.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
    s.connect((HOST, PORT))
    print("Connected to server :)")
except ConnectionRefusedError:
    print("Connection refused :(")
    s.close()
    sys.exit(1)

#tant que le serveur n'a pas envoyé de message, on attend
while True:
    #On reçoit le message
    data = s.recv(1024)
    print("DATA : " + data.decode("utf-8"))
    shot = int(input ("quel case allez-vous jouer ? "))
    shot = str(shot).encode("utf-8")
    s.send(shot)
    #Si le message est vide, on quitte
    if not data:
        print("Connection closed by server")
        break
    #Sinon on affiche le message
    print(data.decode("utf-8"))

#send data to server
s.sendall(b'Hello, world')
#receive data from server
data = s.recv(1024)
s.close()
