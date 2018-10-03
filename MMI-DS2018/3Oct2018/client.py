import socket
import threading
import sys

class Client():
    BUF_SIZE = 1024
    def __init__(self, server_addr):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = server_addr 
        self.socket.connect(self.server_addr)
    
    def send(self, msg):
        self.socket.send(msg.encode())
    
    def recv(self):
        data = self.socket.recv(self.BUF_SIZE)
        return data.decode('utf-8')

if __name__ == '__main__':
    server_addr = (sys.argv[1], int(sys.argv[2]))
    print('Connecting in {}'.format(server_addr))
    client = Client(server_addr)
    while True:
        # Send data
        message = input('>> ')
        client.send(message)
        msg = client.recv()
        if msg == '/quit':
            print('Disconnected')
            break
        print(msg)