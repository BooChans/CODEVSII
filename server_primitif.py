# -*- coding: utf-8 -*-

import socket

UDP_IP = "192.168.43.129"
UDP_PC = "192.168.43.84"
UDP_PORT = 2390
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP   
s.sendto(bytes("Salut",'utf-8'),(UDP_PC,2390))