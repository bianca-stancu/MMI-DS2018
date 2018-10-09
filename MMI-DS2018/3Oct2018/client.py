import socket
import threading
import sys
import chat_protobuf_pb2

class ClientMessage:
    def encode(self,to,fr,msg):
        my_message = chat_protobuf_pb2.Message()
        my_message.fr = fr
        my_message.to = 0 #temporary
        my_message.message = msg 
        to_send = my_message.SerializeToString()
        return to_send

    def decode(self,buf):
        my_Message = chat_protobuf_pb2.Message()
        my_Message.ParseFromString(buf)
        return my_Message.message

class Client():
    BUF_SIZE = 1024
    def __init__(self, server_addr):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = server_addr 
        self.socket.connect(self.server_addr)
        server_given_id = self.socket.recv(self.BUF_SIZE)
        self.client_id = int(server_given_id.decode('utf-8'))
        print('My user id: {}'.format(self.client_id))
    
    def send(self, msg):
        client_message = ClientMessage()
        client_id = self.client_id
        self.socket.send(client_message.encode(0,client_id,msg))
    
    def recv(self):
        data = self.socket.recv(self.BUF_SIZE)
        client_message = ClientMessage()
        return client_message.decode(data)

if __name__ == '__main__':
    server_addr = (sys.argv[1], int(sys.argv[2]))
    print('Connecting in {}'.format(server_addr))
    client = Client(server_addr)
    while True:
        # Send data
        message = input('>>')
        client.send(message)
        msg = client.recv()
        if msg  == '/quit':
            print('Disconnected')
            break
        print(msg)