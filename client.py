# basic-python-chatroom: client.py
# by Michael White (MikeJamesWhite on Github)
#
# A client which can connect to a server and receive responses until an exit
# signal is sent. 
#
# v0.03

import socket
import select
import curses
from threading import Thread

# curses init
curses.LINES = 0
curses.COLS = 0
stdscr = curses.initscr()
stdscr.keypad(True)
curses.echo()
begin_x = 0; begin_y = 2
height = curses.LINES - 3
width = curses.COLS - 1
titleWin = curses.newwin(1, width, 0, 0)
titleWin.addstr("basic-python-chatroom client v0.03 - by Mike White")
titleWin.refresh()
chatWin = curses.newwin(height, width, begin_y, begin_x)
typeWin = curses.newwin(1, width, curses.LINES - 1, 0)

# default variables
PORT = 5090
HOST = "mike-zenbuntu"

def broadcast_receiver(serverSocket):
    while (True):
        serverSocket.settimeout(4)
        try:
            chatOutput((serverSocket.recv(1024).decode()))
        except:
            return

def onExit():
    stdscr.keypad(False)
    curses.endwin()


def chatOutput(outStr):
    chatWin.addstr(outStr + "\n")
    #chatWin.clrtoeol()
    chatWin.refresh()

def userInput(inStr):
    typeWin.addstr(inStr)
    typeWin.refresh()
    s = typeWin.getstr().decode()
    typeWin.erase()
    typeWin.refresh()
    return s

def main():
    global HOST, PORT
    alias = userInput("Enter your alias: ")
    connected = False
    while (not connected):
        userin = userInput("Custom host and port? (y/n): ")
        if (userin == 'y'):
            HOST = userInput("Enter the host: ")
            PORT = int(userInput("Enter the port number: "))
        serverSocket = socket.socket()
        try:
            serverSocket.connect((HOST, PORT))
            connected = True
        except:
            typeWin.addstr("Error: connection failed. ")

    receiverThread = Thread(target = broadcast_receiver, args = (serverSocket, ))
    receiverThread.start()
    userin = ""
    while (userin != "exit"):
        userin = userInput(alias + "> ")
        serverSocket.send(userin.encode())
    onExit()
    serverSocket.close()

if __name__ == '__main__':
    main()