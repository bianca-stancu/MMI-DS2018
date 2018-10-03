import socket
from threading import Lock, Thread

number_users = 0
lock = Lock()

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
    
    
    def run(self):
        while True:
            try:
                buf = self.socket.recv(self.BUF_SIZE)
                decoded_str = buf.decode('utf-8')
                if decoded_str == '/quit':
                    self.socket.send(buf)
                    self.socket.close()
                    global number_users
                    lock.acquire()
                    number_users-= 1
                    lock.release() 
                    break
                self.socket.send(buf)
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

    