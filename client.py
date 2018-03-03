# basic-python-chatroom: client.py
# by Michael White (MikeJamesWhite on Github)
#
# A client which can connect to a server, send messages and receive broadcasts until an exit
# signal is sent. 
#
# v0.06

import socket
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
titleWin.addstr("basic-python-chatroom client v0.06 - by Mike White")
titleWin.refresh()
chatWin = curses.newwin(height, width, begin_y, begin_x)
chatPad = curses.newpad(500, curses.COLS - 1)
chatPadPos = 0
typeWin = curses.newwin(1, width, curses.LINES - 1, 0)
maxChatPadPos = -height

# default variables
PORT = 50050
HOST = "kingkong.zapto.org"
receiving = True

def broadcast_receiver(serverSocket):
    while (receiving):
        serverSocket.settimeout(30)
        try:
            chatOutput((serverSocket.recv(1024).decode()))
        except:
            continue

def onExit():
    stdscr.keypad(False)
    curses.endwin()


def chatOutput(outStr):
    global chatPadPos, maxChatPadPos
    maxChatPadPos += 1
    chatPad.addstr(outStr + "\n")
    if chatPadPos <= maxChatPadPos:
        chatPadPos += 1
    chatPad.refresh(chatPadPos, 0, begin_y, begin_x, height, width)
    titleWin.refresh()
    typeWin.refresh()

def userInput(inStr):
    typeWin.addstr(inStr)
    typeWin.refresh()
    s = typeWin.getstr().decode()
    typeWin.clrtoeol()
    typeWin.refresh()
    return s

def main():
    global HOST, PORT, receiving, chatPadPos, height, width, begin_x, begin_y, maxChatPadPos
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
    cmd = ''
    while (True):
        curses.cbreak()
        curses.noecho()
        typeWin.keypad(True)
        cmd = typeWin.getch()
        while (cmd != ord(' ')):
            cmd = typeWin.getch()
            if  (cmd == curses.KEY_DOWN):
                if chatPadPos <= maxChatPadPos:
                    chatPadPos += 1
                    chatPad.refresh(chatPadPos, 0, begin_y, begin_x, height, width)
            elif (cmd == curses.KEY_UP):
                if chatPadPos > 0:
                    chatPadPos -= 1
                    chatPad.refresh(chatPadPos, 0, begin_y, begin_x, height, width)
        curses.echo()
        curses.nocbreak()
        typeWin.keypad(False)

        userin = alias + "> " + userInput(alias + "> ")
        serverSocket.send(userin.encode())
        if (userin[-6:] == "exit()"):
            receiving = False
            onExit()
            serverSocket.close()
            exit()

if __name__ == '__main__':
    main()