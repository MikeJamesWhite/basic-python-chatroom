# basic-python-chatroom: client.py
# by Michael White (MikeJamesWhite on Github)
#
# A client which can connect to a server and receive responses until an exit
# signal is sent. 
#
# v0.01

import socket
import select
from threading import Thread

name = "" # client name
PORT = 5090
HOST = "mike-zenbuntu"
receiving = True

def broadcast_receiver(serverSocket):
    while (receiving):
        serverSocket.settimeout(2)
        try:
            print(serverSocket.recv(1024).decode())
        except:
            return

def main():
    name = input("Enter your alias: ")

    serverSocket = socket.socket()
    serverSocket.connect((HOST, PORT))
    receiverThread = Thread(target = broadcast_receiver, args = (serverSocket, ))
    receiverThread.start()
    userin = ""
    while (userin != "exit"):
        userin = input(name + "> ")
        serverSocket.send(userin.encode())
    serverSocket.close()
    receiving = False

if __name__ == '__main__':
    main()