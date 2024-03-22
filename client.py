# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 22:21:12 2024

@author: baoch
"""

import socket 
UDP_IP = "127.0.0.1"
UDP_PORT = 2390
MESSAGE = b"Hello, World from the client!"
print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)
MESSAGE = input("Saisir un nombre")
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(bytes(MESSAGE,"utf-8"), (UDP_IP, UDP_PORT))