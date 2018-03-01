import socket

def main():
    s = socket.socket()
    host = socket.gethostname()
    soc = 5090
    s.bind((host, soc))
    print("Server: Bound to address:",host,soc)
    s.listen()
    print("Server: Listening for TCP connections!")
    while(True):
        print("Server: Waiting for a connection...")
        client, addr = s.accept()
        print("Server: Got connection from", addr)
        client.send("Server: Welcome to the room!".encode())
        message = client.recv(1024).decode()
        while (message != "exit"):
            print("Client: ", message)
            client.send('Server: Got your message!'.encode())
            message = client.recv(1024).decode()
        print("Server: Client closed connection.")

if __name__ == '__main__':
    main()