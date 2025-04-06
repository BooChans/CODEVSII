# -*- coding: utf-8 -*-

import socket


UDP_IP = "192.168.43.129"
UDP_PC = "192.168.43.84"
ETH_PC = "192.168.8.137"
UDP_PORT = 2390
MESSAGE = input("Saisir un nombre")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP   
s.bind(('',UDP_PORT))  
s.connect(('192.168.8.100',2390))
s.sendall(bytes(MESSAGE,'utf-8'))
data,addr=s.recvfrom(1024)
data=str(data,"utf-8")
print(data,addr)
data,addr=s.recvfrom(1024)
data=str(data,"utf-8")
print(data)
s.sendto(bytes(data,'utf-8'),(UDP_IP,UDP_PORT))
data,addr=s.recvfrom(1024)
data=str(data,"utf-8")
print(data)
