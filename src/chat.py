import socket
import threading
import sys
import time

class Server(threading.Thread):
    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Started server!\n")
        hostNode = ''
        port = 51001
        self.sock.bind((hostNode, port))
        self.sock.listen(1)
        print("Listening on port %d\n" %port)
        (clientname, address) = self.sock.accept()
        print("Connection from %s\n" % str(address))
        while 1:
            chunk = clientname.recv(1024)
            print(str(address) + ':' + chunk)

class Client(threading.Thread):
    def connect(self, host, port):
        self.sock.connect((host, port))
    def client(self, host, port, message):
        sent = self.sock.send(message)
        print("Message sent\n")
    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            host = input("Enter the hostname\n>>")
            port = int(input("Enter the port number\n>>"))
        except EOFError:
            print("Error occurred!")
            return 1

        print("Connecting...\n")
        s = ''
        self.connect(host, port)
        print("Connected succesfully!\n")
        while 1:
            print("Waiting for message\n")
            message = raw_input('>>')
            if message == 'exit':
                break
            if message == '':
                continue
            print("Sending message...\n")
            self.client(host, port, message)
        return(1)

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
