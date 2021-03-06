# basic-python-chatroom: server.py
# by Michael White (MikeJamesWhite on Github)
#
# A server app which allows clients to connect, receives messages and rebroadcasts those
# messages to all connected clients.
#
# v0.06

import socket
from threading import Thread

clients = [] # list of all current clients
PORT = 50050

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
        decoded = message.decode()
        print(decoded)
        if (decoded[-6:] == "exit()"):
            print("Server> Client disconnected.")
            clients.remove(client)
            name = "Server> " + decoded[0:decoded.find('>')] + " left the room."
            message = name.encode()
        thread = Thread(target = broadcast_to_clients, args = (message, ))
        thread.start()

def accept_clients(serverSocket):
    print("Server> Accepting connections...")
    while True:
        client, addr = serverSocket.accept()
        clients.append(client)
        thread = Thread(target = listen_to, args = (client, ))
        thread.start()
        print("Server> Accepted new client from", addr)

def main():
    print('\033[H\033[J') # clear terminal
    print("basic-python-chatroom: server.py v0.06\n")
    global PORT
    userin = input("Custom port? (y/n) ")
    if (userin == 'y'):
        PORT = int(input("Enter port number: "))
    serverSocket = socket.socket()
    host = socket.gethostname()
    serverSocket.bind(('', PORT))
    print("Server> Bound to address '", host, ": ", PORT, sep ='', end ="'\n")
    serverSocket.listen()
    print("Server> Initialised TCP listener.")
    accept_clients(serverSocket)

if __name__ == '__main__':
    main()