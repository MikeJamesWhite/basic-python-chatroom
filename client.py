import socket

def main():
    s = socket.socket()
    s.connect(("mike-zenbuntu", 5090))
    print(s.recv(1024).decode())
    userin = input("Enter a message: ")
    s.send(userin.encode())
    while (userin != "exit"):
        print (s.recv(1024).decode())        
        userin = input("Enter a message: ")
        s.send(userin.encode())
    s.close()

if __name__ == '__main__':
    main()