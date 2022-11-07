#!/usr/bin/python3
import sys
import socket

class tcp:
    def tcpConnexion():
        s = socket.socket(socket.AF_INET6 ,socket.SOCK_STREAM, 0)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host = "localhost"
        port = 7777


        s.bind((host, port))

        s.listen(1)

        while(True):
            newSocket, addr = s.accept()
            while(True):
                data = newSocket.recv(1500)
                if(data==b""):
                    s.close()
                    break
                else:
                    newSocket.send(data)
        


            


