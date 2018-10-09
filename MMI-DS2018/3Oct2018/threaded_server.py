import socket
from threading import Lock, Thread
import chat_protobuf_pb2
import handshake_pb2

number_users = 0
users_id = set()
lock = Lock()

class ServerMessage:
    def decode(self,buf):
        my_Message = chat_protobuf_pb2.Message()
        my_Message.ParseFromString(buf)
        ##print('to:{},from:{},message:{}'.format(my_Message.to,my_Message.fr,my_Message.message))
        return (my_Message.message,my_Message.fr)
    
    def encode(self,to,fr,msg):
        my_message = chat_protobuf_pb2.Message()
        my_message.fr = fr
        my_message.to = 0 #temporary
        my_message.message = msg 
        to_send = my_message.SerializeToString()
        return to_send

class ServerHandshake:
    def encode(self,client_id,error):
        print('Handshake response for id {}: error = {}'.format(client_id,error))
        handshake = handshake_pb2.Handshake()
        handshake.id = client_id
        handshake.error = error
        to_send = handshake.SerializeToString()
        return to_send

    def decode(self,buf):
        handshake = handshake_pb2.Handshake()
        handshake.ParseFromString(buf)
        return handshake.id


class ClientThread(Thread):
    BUF_SIZE = 1024
    def __init__(self, ip, port, socket):
        # super(self)
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket
        global number_users
        lock.acquire()
        number_users+= 1
        lock.release()
        buf = self.socket.recv(self.BUF_SIZE)
        server_handshake = ServerHandshake()
        global users_id
        lock.acquire()
        if server_handshake.decode(buf) in users_id:
            self.socket.send(server_handshake.encode(server_handshake.decode(buf), True))
            self.socket.close()
        else:
            users_id.add(server_handshake.decode(buf))
            self.socket.send(server_handshake.encode(server_handshake.decode(buf), False))
        lock.release()
    

    def run(self):
        client_message = ServerMessage()
        while True:
            try:
                buf = self.socket.recv(self.BUF_SIZE)
                (decoded_str,decoded_fr)=client_message.decode(buf)
                if decoded_str == '/quit':
                    print("Client disconnected!")
                    self.socket.send(client_message.encode(decoded_fr,0,decoded_str))
                    self.socket.close()
                    global number_users
                    lock.acquire()
                    number_users-= 1
                    lock.release() 
                    global users_id
                    lock.acquire()
                    users_id.remove(decoded_fr)
                    lock.release() 
                    break
                self.socket.send(client_message.encode(decoded_fr,0,buf))
            except:
                self.socket.close()
                break

class ServerThread(Thread):
    def run(self):
        while True:
            try:
                command = input()
                if (command == "/nusers"):
                    print(number_users)
            except Exception as e: 
                print(e)

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(('0.0.0.0', 8080))

server_thread = ServerThread()
server_thread.start()

while True:
    try:
        srv.listen(1)
        print('Starting...')
        conn, addr = srv.accept()
        new_thread_client = ClientThread('127.0.0.1', 8080, conn)
        new_thread_client.start()
    except Exception as e: 
        print(e)
        srv.close()
        print('Terminating server...')
        break

    