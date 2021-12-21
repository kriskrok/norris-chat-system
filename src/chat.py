import socket
import threading
import os
import time
import pickle

#Required env variables
host = os.environ['HOSTNAME'] #IP for current Leader
my_ip = os.environ['MYIP'] #This machine external IP
leader_flag = True if os.environ['LEADER'] == 'True' else False #Is this node leading?

port = 50001
udp_port = 50002
clients = [] #collection of client sockets
nicknames = [] #tuple with (address, 'nick')

class Server(threading.Thread):

    def __init__(self, client_thread):
        #print('Hello from server init')
        threading.Thread.__init__(self) #this is required
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_timestamp = 0
        self.server_socket = None
        self.client_thread = client_thread

    #Server starts for every node, but only one is the Leader. Handle it and the election here
    #This is called when the server class assumes its rightfull place as dear Leader
    def init_leader_functionality(self, hostip=host):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((hostip, port))
        self.server_socket.listen(5)
        #print('clientThread: ', self.client_thread)

    def init_client_heartbeat(self):
        self.udp_socket.bind(('', udp_port))

    #Alas, appears to get stuck on after starting a new client, i.e., hangs.
    def change_leader(self):
        global host
        self.new_host = nicknames[1][0]
        #nicknames.remove[0]
        
        if self.new_host == my_ip:
            #print('new host is me')
            if self.server_socket is not None:
                self.server_socket.close()
                time.sleep(2)
            self.init_leader_functionality(self.new_host)
            #print('I am the captain now')
            self.server_timestamp = time.time()

            self.client_thread.join(1) #param in seconds to timeout
            time.sleep(1)
            #print('Client thread is alive : ', self.client_thread.is_alive())
            host = self.new_host
            
            accept_thread = threading.Thread(target=self.accept)
            accept_thread.start()

            client = Client()
            client.start()


    # This method finds out if ping timestamp is older than 15 seconds.
    def check_host_ping_time(self):
        while True:
            time.sleep(16)
            time_delta = time.time() - self.server_timestamp
            if time_delta > 15:
                #print(f'Host is dead, very dead been for {time_delta} seconds. Long live the host')
                self.change_leader()
                break
            else:
                #print("Host seems healthy")
                #print(nicknames)
                pass
    
    # This method only listens incoming pings from leader and update timestamp when ping arrives.
    # If ping never arrives, wait will never end.
    def receive_ping(self):
        global nicknames
        while True:
            try:
                message, address = self.udp_socket.recvfrom(1024) # buffer size is 1024 bytes
                message = pickle.loads(message)
                #print("received message: %s" % message) #Remove when everything is ok.
                if type(message) == list:
                    nicknames = message
                    #print('Received updated client list: ', nicknames)
                elif message == 'ping':
                    self.server_timestamp = time.time()
            except:
                print("An error occured, the final days are upon us!")
            

    def ping(self, address):
            while True:
                time.sleep(10)
                try:
                    self.udp_socket.sendto(pickle.dumps('ping'), (address[0], udp_port))
                    #print('Pinged')
                    self.udp_socket.sendto(pickle.dumps(nicknames), (address[0], udp_port))
                except:
                    #print("Ping failed!")
                    break

    #WIP, had a succesfull dry-run, needs to be tested on multi-user env
    def send_client_list(self):
        for client in clients:
            #print('Sending client list to: ', client.getpeername()[0])
            #print('Hello from send_client_list', nicknames)
            self.udp_socket.sendto(pickle.dumps(nicknames), (client.getpeername()[0], udp_port))

    # Broadcast message to every client
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
            client_socket, address = self.server_socket.accept() #address is a tuple ('IP', internal_port_num)
            #print("A new connection from {}".format(str(address[0])))
            
            # Ask nickname
            client_socket.send(pickle.dumps('NICK'))
            nickname = pickle.loads(client_socket.recv(1024))
            nicknames.append((address[0], nickname))
            clients.append(client_socket)

            # Print nickname
            self.broadcast(pickle.dumps("{} joined the frey!\n".format(nickname)))
            client_socket.send(pickle.dumps('Connected to server!'))

            self.send_client_list()
            # Start thread for this client
            user_thread = threading.Thread(target=self.handle, args=(client_socket, ))
            user_thread.start()
            ping_thread = threading.Thread(target=self.ping, args=(address, ))
            ping_thread.start()

            #TODO: update new client to rest of the clients
            #self.send_client_list() | test me!

    def run(self):
        if leader_flag:
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
    def __init__(self):
        threading.Thread.__init__(self)

    def init_client_functionality(self):
        global host
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #print('Attempting to connect to host: ', host)
            self.client_socket.connect((host, port))
        except ConnectionRefusedError as err:
            raise SystemExit('Could not connect to leader %s, exiting.' % err)
        # Choose nickname
        self.nickname = input("Kindly provide a nickname: ")    

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
            if message.endswith('quit'):
                self.client_socket.close()
                #Alas neither quit(), exit(), nor raise SystemExit appear to work here
                #would require proper thread management for a gracefull shutdown option

            self.client_socket.send(pickle.dumps(message))
    
    def run(self):
        self.init_client_functionality()
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()
        self.write_thread = threading.Thread(target=self.write)
        self.write_thread.start()
        print("\tClient started!")

if __name__=='__main__':

    client = Client()
    server = Server(client_thread=client)
    server.daemon = True
    print("\tStarting server...")
    server.start()
    time.sleep(1)
  
    print("\tStarting client...")  
    client.start()
