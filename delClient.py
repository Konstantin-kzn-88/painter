import socket
import json

def recvall(sock):
    BUFF_SIZE = 4096  # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) == 0:
            break
    return data


var = 8000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 8888))
str_json = json.dumps((1, [i for i in range(5)]))
sock.sendall(bytes(str_json, encoding='utf-8'))
res = recvall(sock)
var = json.loads(res)
print(var)
sock.close()