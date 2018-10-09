import socket
import threading
import sys
import chat_protobuf_pb2
import handshake_pb2

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

class ClientHandshake:
    def encode(self,client_id):
        print('Handshake attempt with id: {}'.format(client_id))
        handshake = handshake_pb2.Handshake()
        handshake.id = client_id
        handshake.error = False
        to_send = handshake.SerializeToString()
        return to_send

    def decode(self,buf):
        handshake = handshake_pb2.Handshake()
        handshake.ParseFromString(buf)
        return handshake.error

class Client():
    BUF_SIZE = 1024
    def __init__(self, server_addr,client_id):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = server_addr 
        self.socket.connect(self.server_addr)
        client_handshake = ClientHandshake()
        self.socket.send(client_handshake.encode(int(sys.argv[3])))
        server_response = self.socket.recv(self.BUF_SIZE)
        if client_handshake.decode(server_response) is True:
            print('An error has occured, you are not connected!')
            self.connected = False
        else:
            self.client_id = int(sys.argv[3])
            self.connected = True
    
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
    client = Client(server_addr,int(sys.argv[3]))
    while client.connected:
        # Send data
        message = input('>>')
        client.send(message)
        msg = client.recv()
        if msg  == '/quit':
            print('Disconnected')
            break
        print(msg)