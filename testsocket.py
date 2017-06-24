# Testing socket lib

import socket
import os
import fire

socket.setdefaulttimeout(2)

def getbanner(ip='127.0.0.1', port=21):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        data = s.recv(1024)
    return data.decode('utf-8')

# data = getbanner('127.0.0.1', 21)
# print('Received', repr(data))

if __name__ == '__main__':
    if os.environ.get('PYCHARM_HOSTED'):
        data = getbanner()
        print(data)
    else:
        fire.Fire(getbanner)

# with open('README.md', 'r') as f:
#     lines = f.readlines()
# print(lines)