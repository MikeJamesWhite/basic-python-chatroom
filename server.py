# basic-python-chatroom: server.py
# by Michael White (MikeJamesWhite on Github)
#
# A server which allows a client to connect, receives messages and sends acknowledgement
# back to the client.
#
# v0.02

import socket
from threading import Thread

clients = [] # list of all current clients
PORT = 5090

def broadcast_to_clients(message):
    for client in clients:
        try:
            client.send(message)
        except:
            print("Server> Client disconnected.")
            clients.remove(client)

def listen_to(client):
    while True:
        message = client.recv(1024)
        if (message.decode() == "exit"):
            print("Server> Client disconnected.")
            clients.remove(client)
            return
        thread = Thread(target = broadcast_to_clients, args = (message, ))
        thread.start()

def accept_clients(serverSocket):
    print("Server> Accepting connections...")
    while True:
        client, addr = serverSocket.accept()
        thread = Thread(target = listen_to, args = (client, ))
        thread.start()
        clients.append(client)
        print("Server> Accepted new client from", addr)

def main():
    print('\033[H\033[J')
    print("basic-python-chatroom: server.py v0.01\n")
    serverSocket = socket.socket()
    host = socket.gethostname()
    serverSocket.bind((host, PORT))
    print("Server> Bound to address '", host, ": ", PORT, sep ='', end ="'\n")
    serverSocket.listen()
    print("Server> Initialised TCP listener.")
    accept_clients(serverSocket)

if __name__ == '__main__':
    main()