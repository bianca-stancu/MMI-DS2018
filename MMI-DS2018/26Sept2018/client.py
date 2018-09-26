import socket

BUF_SIZE = 1024
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1',8080))
inp = input('>>')
sock.send(inp.encode())
msg = sock.recv(BUF_SIZE)
print(msg.decode("utf-8"))