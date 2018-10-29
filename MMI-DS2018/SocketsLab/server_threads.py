import socket
from threading import Thread
from time import sleep
BUF_SIZE = 1024

import threading

class MyThread(threading.Thread):
    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.conn = conn
        
    def run(self):
        while True:
            buf = self.conn.recv(BUF_SIZE)
            self.conn.send(buf)
        
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
srv.bind(('127.0.0.1',8080))
while True: 
    srv.listen(1)
    conn, addr = srv.accept()
    c = MyThread(conn)
    c.start()