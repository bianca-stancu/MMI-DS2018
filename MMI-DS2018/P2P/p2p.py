import socket
import threading
import protocol_pb2
import sys
import uuid
import datetime
import time


class ClientThread(threading.Thread):
    BUF_SIZE = 1024

    def __init__(self, socket,ip,port):
        threading.Thread.__init__(self)
        self.socket = socket
        self.ip = ip
        self.port = port
        self.alive = True

    def send(self, msg):
        self.socket.send(msg.SerializeToString())

    def recv_msg(self):
        data = self.socket.recv(self.BUF_SIZE)
        msg = protocol_pb2.P2PMessage()
        msg.ParseFromString(data)
        return msg
            

    def handshake(self):
        global 
        msg = protocol_pb2.Peer(fr_ip=my_address[0], fr_port = my_address[1],to_ip=self.ip, to_port= self.port)
        self.send(msg)
        data = self.socket.recv(self.BUF_SIZE)
        msg.ParseFromString(data)
        print("Added peer")
        self.num = len(peers)
        peers.append(self)
    
    def wait_for_handshake(self):
        global peers
        buf = self.socket.recv(self.BUF_SIZE)
        msg = protocol_pb2.Peer()
        msg.ParseFromString(buf)
        handshake_msg = protocol_pb2.Peer(fr_ip=my_address[0], fr_port = my_address[1],to_ip=msg.fr_ip, to_port= msg.fr_port)
        print("Received request to add peer from {}:{}".format(msg.fr_ip,msg.fr_port))
        self.socket.send(handshake_msg.SerializeToString())
        self.ip = msg.fr_ip
        self.port = msg.fr_port
        self.num = len(peers)
        peers.append(self)

    def run(self):
        global peers
        while self.alive:
            try:
                msg = self.recv_msg()
                if (not msg.HasField("uuid_ack")) and (msg.msg is None or msg.msg == ""):
                    self.close_client()
                else:
                    if msg.uuid in uuids:
                        continue
                    uuids[msg.uuid] = (datetime.datetime.now(),msg)
                    if msg.HasField("uuid_ack"):
                        acked.add(msg.uuid_ack)
                        acked.add(msg.uuid)
                    if msg.to == my_name:
                        if msg.HasField("msg"):
                            print("From {}: {}".format(msg.fr,msg.msg))
                            ack_message = protocol_pb2.P2PMessage(fr = msg.fr,to=msg.to, uuid=str(uuid.uuid4()), uuid_ack=msg.uuid)
                            self.broadcast(ack_message)
                    else:
                        self.broadcast(msg)
            except Exception as e:
                pass
    
    def broadcast(self, msg):
        for i in range(len(peers)):
            if i == self.num and msg.HasField('msg'):
                continue
            peers[i].send(msg)

    def close_client(self):
        print("Closed connection with: {}:{}".format(self.ip,self.port))
        global peers
        self.socket.close()
        del peers[self.num]
        self.alive = False

class ServerThread(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srv.bind((ip, port))
        self.alive = True

    def run(self):
        while self.alive:
            try:
                self.srv.listen(1)
                conn,address= self.srv.accept()
                client_ip = address[0]
                client_port = address[1]
                client_thread = ClientThread(conn,client_ip,client_port)
                client_thread.wait_for_handshake()
                client_thread.daemon = True
                client_thread.start()
            except:
                pass
    
    def close_server(self):
        self.alive = False
        self.srv.close()

def showHelp():
    print("Here's a list of commands you can do:")
    print("To add another client as a peer: add <ip> <port>")
    print("To close a connection with a peer and remove it: close <ip> <port>")
    print("To send a message to someone: send <ip> <port>")

class ResendMessages(threading.Thread):
    def run(self):
        while True:
            for i in (set(str(s) for s in uuids.keys()) - acked):
                if (datetime.datetime.now()-uuids[i][0]).total_seconds() >= 5:
                    for client in peers:
                        p2pmsg = uuids[i][1]
                        client.send(p2pmsg)
            time.sleep(5)

    def close_server(self):
        self.alive = False
        self.srv.close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: {} <ip> <port> <display_name>'.format(sys.argv[0]))
        sys.exit(1)
    peers = []
    uuids = {}
    acked = set()
    server_thread = ServerThread(sys.argv[1], int(sys.argv[2]))
    my_address=(sys.argv[1],int(sys.argv[2]))
    my_name = sys.argv[3]
    server_thread.daemon = True
    server_thread.start()
    resend_thread = ResendMessages()
    resend_thread.daemon = True
    resend_thread.start()

    while True:
        cmd = input()
        if cmd == '/nusers':
            print('Users: {}'.format(len(peers)))
        elif cmd == "help":
                showHelp()
        elif cmd == "exit":
            print("Finishing program...")
            break
        else:
            commands = cmd.split()
            if commands[0] == "add":
                try:
                    ip = commands[1]
                    port = int(commands[2])

                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((ip, port))

                    c = ClientThread(sock, ip, port)
                    c.handshake()
                    c.daemon = True
                    c.start()
                except:
                    print("Sorry, your request could not be processed")
            elif commands[0]=="send":
                try:
                    to_name = commands[1]
                    message = input("message:")
                    found = False
                    uuidstr = str(uuid.uuid4())
                    msg = protocol_pb2.P2PMessage(fr = my_name,to=to_name, msg=message, uuid=uuidstr)
                    uuids[msg.uuid] = (datetime.datetime.now(),msg)
                    for i in range(len(peers)):
                        peers[i].send(msg)
                except Exception as e:
                    print("Sorry, your request could not be processed") 
                    print(e)
            elif commands[0]=="close":
                try:
                    address_ip = commands[1]
                    address_port = int(commands[2])
                    found = False
                    for i in range(len(peers)):
                      if peers[i].ip == address_ip and peers[i].port == address_port:
                            msg = protocol_pb2.P2PMessage(fr = "",to="", msg="", uuid="")
                            peers[i].send(msg)
                            peers[i].close_client()
                            found = True
                    if not found:
                        print("Sorry, this client is not in your list, cannot delete it!")
                except:
                    print("Sorry, your request could not be processed")
    sys.exit()