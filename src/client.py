import socket
import threading
import os

# Choose nickname
nickname = input("Choose your nickname: ")
hostname = os.environ['HOSTNAME']

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((hostname, 50001))

# Listen server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

# Send messages
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

# Threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
