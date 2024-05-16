# -*- coding: utf-8 -*-

import socket


codes={}
UDP_IP = "192.168.43.129"
UDP_PC = "192.168.43.84"
UDP_PORT = 2390
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP   
s.bind(('',UDP_PORT))  
while True:              
    data,addr=s.recvfrom(1024)
    data=str(data,"utf-8")
    print(data,addr[0])
    if addr[0]=='192.168.43.84':
        data=data.split(" ")
        id_velo = int(data[0])
        code = int(data[1])
        codes[code]=(id_velo,0)
    if addr[0] == '192.168.43.129':
        try:
            code = int(data)
            print(code)
            if code in codes.keys():
                print(code, "accepted")
                s.sendto(bytes(str(codes[code][0]),'utf-8'),(UDP_IP,UDP_PORT)) 
                codes[code]=(codes[code][0],codes[code][1]+1)
        except:
            None
    
    
