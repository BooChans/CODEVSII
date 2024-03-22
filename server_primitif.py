# -*- coding: utf-8 -*-

import socket

UDP_IP = "192.168.43.129"
UDP_PC = "192.168.43.84"
UDP_PORT = 2390
MESSAGE = input("Saisir un nombre")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP   
s.bind(('',UDP_PORT))                 
s.sendto(bytes(MESSAGE,'utf-8'),(UDP_IP,UDP_PORT))
data,addr=s.recvfrom(1024)
data=str(data,"utf-8")
print(data)
