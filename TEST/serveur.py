#!/usr/bin/python3
import socket
import time


#variables

grille =     """
    ______________
   |0   |1   |2   |
   | {}  | {}  | {}  |
   |____|____|____|
   |3   |4   |5   |
   | {}  | {}  | {}  |
   |____|____|____|
   |6   |7   |8   |
   | {}  | {}  | {}  |
   |____|____|____|
   """

empty_grid=[" "," "," "," "," "," "," "," "," "]
tour=0

#ajouter une piece
def add_piece(gridgrid,x,piece):
        gridgrid[x] = piece

#saisie du joueur : la merde, plante s'il tape autre chose qu'un nombre entier
def saisiejoueur(joueur):
        global conn
        if joueur%2 == 0:
                case = int(conn.recv(1024).decode())
                while case>8 or grid[case]!=0:
                        if case>8:
                                printjoueur("Taper un numero entre 0 et 8",joueur)
                                case = int(conn.recv(1024).decode())
                        elif grid[case]!=0:
                                printjoueur("Il y a deja un jeton la case {}".format(case),joueur)
                                case = int(conn.recv(1024).decode())
                print ("from connected  user: " + str(case))
                        
        else:
                while 1:
                        try:
                                inst = input(" ? ")
                                inst = int(inst)
                                if not(0<= inst <= 8):
                                        raise ValueError()
                                case = int(inst)
                                break
                        except ValueError:
                                print("Un NOMBRE entre 0 et 8 ! ")
                while case>8 or grid[case]!=0:
                        if case>8:
                                printjoueur("Taper un numero entre 0 et 8",joueur)
                                case = int(input(" ? "))
                        elif grid[case]!=0:
                                printjoueur("Il y a deja un jeton la case {}".format(case),joueur)
                                case = int(input(" ? "))
                print ("from connected  user: " + str(case))

        return case
#communication
#tous les joueurs
def printall(msg):
        global conn
        print(msg)
        conn.send(msg.encode())

#le client seulement
def printclient(msg):
        global conn
        conn.send(msg.encode())

#celui dont c'est le tour
def printjoueur(msg,joueur):
        global conn
        if joueur%2 == 0:
                printclient(msg)
        else:
                print(msg)

#affichage de la grille - doit pouvoir se faire bcp plus  simplement que cette merde
def print_grid(gridgrid):
        global conn
        #on cree une liste vide qui sera remplie avec les symboles
        grid_to_print=[]
        for n,i in enumerate(gridgrid):
                if i==0:
                        grid_to_print.append(' ')
                elif i==1:
                        grid_to_print.append('X')
                elif i==4:
                        grid_to_print.append('O')
        #elle est affichee au serveur et au client
        print( grille.format(*tuple(grid_to_print)) )
        conn.send(grille.format(*tuple(grid_to_print)).encode())

#detecter la victoire la victoire
def victoire(list_test):
        #somme des lignes, des colonnes, des diagonales
        #initialisation des totaux
        c1,c2,c3 = 0,0,0 
        l1=sum(list_test[0:3]) #ligne 1
        l2=sum(list_test[3:6]) #ligne 2
        l3=sum(list_test[6:9]) #ligne 3
        for i in range(3):
                c1+=list_test[3*i] #colonne 1
                c2+=list_test[3*i+1] #colonne 2
                c3+=list_test[3*i+2] #colonne 3
        d1=list_test[0]+list_test[4]+list_test[8] #diag 1
        d2=list_test[6]+list_test[4]+list_test[2] #diag 2
        scores=[l1,l2,l3,c1,c2,c3,d1,d2]
        if 3 in scores: #1+1+1 = 3 : le joueur 1 gagne
                printall("Joueur 1 a gagne !")
                return(2)
        elif 12 in scores: #4+4+4 = 12 : le joueur 2 gagne
                printall("Joueur 2 a gagne !")
                return(1)
        elif not 0 in list_test: #toutes les cases sont occupees : match nul
                printall("Match nul !")
                return(3)
        else:
                return(0)

#initialisation des variables
def init_game():
        global empty_grid
        global grid
        global tour
        vainqueur=0
        #reset de la grille
        grid=empty_grid
        for i in range(9):
                add_piece(grid,i,0)
        printclient("Bienvenue ! Vous etes le joueur 1")
        print("Bienvenue ! Vous etes le joueur 2")

#la partie elle meme
def jouer():
        global grid
        global tour
        global conn

        #on ouvre le socket... et on attend le client
        #serveur socket
        host = "127.0.0.1"
        port = 5001
                
        mySocket = socket.socket()
        mySocket.bind((host,port))
               
        mySocket.listen(2)
        conn, addr = mySocket.accept()
        print ("Connexion de : " + str(addr))

        #initialisation de la partie
        init_game()
        #boucle inifinie
        while True:
                #messages aux joueurx
                print_grid(grid) #imprime la grille
                printjoueur("Joueur {}, c'est a vous !".format( (tour%2)+1 ),tour)
                printjoueur("Taper le numero de la case sur laquelle placer votre jeton",tour)
                #saisie du joueur
                case = saisiejoueur(tour)
                #formatage de la grille
                grid[case]=3*(tour%2)+1 #1 si le tour est pair, 4 si le tour est impair
                #test de fin de partie
                vainqueur=victoire(grid)
                tour+=1
                #si la partie est terminee on reinitialise
                if vainqueur!=0:
                        print_grid(grid)
                        printall("Partie terminee. Nouvelle partie ! (ctrl+c pour stop)")
                        init_game()


jouer()