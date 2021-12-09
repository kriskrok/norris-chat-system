import socket
import threading
import os

# Connections
host = os.environ['HOSTNAME']
port = 50001

# Start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Gather client info
clients = []
nicknames = []

# Broadcast messages
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle messages
def handle(client):
    while True:
        try:
            # Send messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # If client not found, remove it
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Listen messages
def receive():
    while True:
        # Accept connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Ask nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start thread for this client
        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()

receive()



