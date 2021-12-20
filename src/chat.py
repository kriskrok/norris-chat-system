import socket
import threading
import os
import time
import pickle

host = os.environ['HOSTNAME'] #IP for current Leader
my_ip = os.environ['MYIP'] #This machine external IP

leaderFlag = False

port = 50001
udp_port = 50002
clients = []
nicknames = []

class Server(threading.Thread):

    def __init__(self):
        print('Hello from server init')
        threading.Thread.__init__(self)
        self.server_socket = ''
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_timestamp = time.time()

    
    def init_leader_functionality(self):
        #Server starts for every node, but only one is the host. Handle it and the election here
        #This is called when the server class assumer its rightfull place as dear Leader
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)

    def init_client_heartbeat(self):
        self.udp_socket.bind(('', udp_port))

    def check_host_ping_time(self):
        while True:
            time.sleep(16)
            time_delta = time.time() - self.server_timestamp
            if time_delta > 15:
                print(f'Host is dead, very dead been for {time_delta} seconds. Long live the host')
            else:
                print("Host seems healthy")
                print(nicknames)
    
    # This should prolly handle heartbeat and all the rest goodies
    def receive_ping(self):
        global nicknames
        while True:
            try:
                message, address = self.udp_socket.recvfrom(1024) # buffer size is 1024 bytes

                message = pickle.loads(message)
                print("received message: %s" % message) #Remove when everything is ok.
                if type(message) == list:
                    nicknames = message
                elif message == 'ping':
                    self.server_timestamp = time.time()
            except:
                print("An error occured, the final days are upon us!")
            

    def ping(self, address):
            while True:
                time.sleep(10)
                try:
                    self.udp_socket.sendto(pickle.dumps('ping'), (address[0], udp_port))
                    print('Pingasin')
                    self.udp_socket.sendto(pickle.dumps(nicknames), (address[0], udp_port))
                except:
                    print("Ping failed!")

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
                self.broadcast(pickle.dumps('{} left!'.format(nickname[0])))
                nicknames.remove(nickname)
                break

    def accept(self):
        while True:
            # Accept connection
            client_socket, address = self.server_socket.accept()
            print("Connected with {}".format(str(address)))

            # Ask nickname
            client_socket.send(pickle.dumps('NICK'))
            nickname = pickle.loads(client_socket.recv(1024))
            nicknames.append((nickname, address))
            clients.append(client_socket)

            # Print nickname
            print("Nickname is {}".format(nickname))
            self.broadcast(pickle.dumps("{} joined!\n".format(nickname)))
            client_socket.send(pickle.dumps('Connected to server!'))

            # Start thread for this client
            user_thread = threading.Thread(target=self.handle, args=(client_socket, ))
            user_thread.start()
            ping_thread = threading.Thread(target=self.ping, args=(address, ))
            ping_thread.start()

    def run(self):
        if leaderFlag:
            self.init_leader_functionality()
            accept_thread = threading.Thread(target=self.accept)
            accept_thread.start()
        else:
            self.init_client_heartbeat()
            receive_ping_thread = threading.Thread(target=self.receive_ping)
            receive_ping_thread.start()
            check_host_ping_thread = threading.Thread(target=self.check_host_ping_time)
            check_host_ping_thread.start()


class Client(threading.Thread):
    #have the threads here as instance variables:
    def __init__(self):
        threading.Thread.__init__(self)
        print('Hello from client init!')

        # Choose nickname
        self.nickname = input("Kindly provide a nickname: ")

        # Connect to server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
    
    def receive(self):
        while True:
            try:
                message = pickle.loads(self.client_socket.recv(1024))
                if message == 'NICK':
                    self.client_socket.send(pickle.dumps(self.nickname))
                else:
                    print(message)
            except:
                print("An error occurred!")
                self.client_socket.close()
                break

    def write(self):
        while True:
            message = '{}: {}'.format(self.nickname, input(''))
            if message == 'quit':
                print()
            self.client_socket.send(pickle.dumps(message))
    
    def run(self):
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()
        self.write_thread = threading.Thread(target=self.write)
        self.write_thread.start()

if __name__=='__main__':

    server = Server()
    server.daemon = True
    print("Starting server...\n")
    server.start()
    time.sleep(1)
    
    print("Starting client...")
    client = Client()
    print("Client started!")
    client.start()