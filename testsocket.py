# Testing socket lib

import socket

socket.setdefaulttimeout(2)

def getbanner(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        data = s.recv(1024)
    return data

data = getbanner('127.0.0.1', 21)
print('Received', repr(data))K