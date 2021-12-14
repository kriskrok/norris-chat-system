import socket
import threading
import os
import time

host = os.environ['HOSTNAME']
errorhost = os.environ['ERRORHOST']
port = 50001
clients = []
nicknames = []

class Server(threading.Thread):
    #Server starts for every node, but only one is the host. Handle it and the election here
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def ping(self):
        while True:
            time.sleep(1)
            try:
                self.host_socket.sendto('hello'.encode('utf8'), (host, port))
                print("Host ping success!")
            except:
                print("Host ping failed!")

    # Broadcast messages
    def broadcast(self, message):
        for client in clients:
            client.send(message)
    
    def handle(self, client):
        while True:
            try:
                # Send messages
                message = client.recv(1024)
                self.broadcast(message)
            except:
                # If client not found, remove it
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                self.broadcast('{} left!'.format(nickname).encode('utf8'))
                nicknames.remove(nickname)
                break

    def run(self):
        while True:
            # Accept connection
            client, address = self.server.accept()
            print("Connected with {}".format(str(address)))

            # Ask nickname
            client.send('NICK'.encode('utf8'))
            nickname = client.recv(1024).decode('utf8')
            nicknames.append(nickname)
            clients.append(client)

            # Print nickname
            print("Nickname is {}".format(nickname))
            self.broadcast(("{} joined!".format(nickname).encode('utf8')))
            client.send('Connected to server!'.encode('utf8'))

            # Start thread for this client
            thread = threading.Thread(target=self.handle, args=(client, ))
            thread.start()
            ping_thread = threading.Thread(target=self.ping)
            ping_thread.start()

class Client(threading.Thread):
    # Choose nickname
    nickname = input("Choose your nickname: ")

    # Connect to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    
    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf8'))
                else:
                    print(message)
            except:
                print("An error occurred!")
                self.client.close()
                break

    def write(self):
        while True:
            message = '{}: {}'.format(self.nickname, input(''))
            self.client.send(message.encode('utf8'))
    
    def run(self):
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        write_thread = threading.Thread(target=self.write)
        write_thread.start()

if __name__=='__main__':
    server = Server()
    server.daemon = True
    print("Starting server...")
    server.start()
    time.sleep(1)
    print("Starting client...")
    client = Client()
    print("Client started!")
    client.start()
