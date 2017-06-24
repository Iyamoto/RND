# Testing socket lib

import socket
import os
import fire
import nmap

socket.setdefaulttimeout(2)

def nmapScan(tgtHost, tgtPort):
    nmScan = nmap.PortScanner()
    nmScan.scan(tgtHost, tgtPort)
    state=nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    return state

def getbanner(ip='127.0.0.1', port=21):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        data = s.recv(1024)
    return data.decode('utf-8')

if __name__ == '__main__':
    if os.environ.get('PYCHARM_HOSTED'):
        # data = getbanner()
        # print(data)
        # print(socket.gethostbyname('ya.ru'))
        # print(socket.gethostbyaddr('8.8.8.8'))
        # scan = nmapScan('127.0.0.1', 21)
        # print(scan)
        exit(1)
    else:
        fire.Fire(getbanner)

# with open('README.md', 'r') as f:
#     lines = f.readlines()
# print(lines)