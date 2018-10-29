import socket
BUF_SIZE = 1024
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
srv.bind(('127.0.0.1',8080))
srv.listen(1)
while True: 
    conn, addr = srv.accept() ##Get a connection
    buf = conn.recv(BUF_SIZE) ##Read 1024 bytes
    conn.send(buf)  ## Send it back to the client
