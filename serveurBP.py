# -*- coding: utf-8 -*-

import socket
import datetime
import sqlite3




codes={}
UDP_IP = "192.168.43.129"
UDP_PC_P40 = "192.168.43.84"
UDP_PC = "10.22.29.2"
UDP_TEST = "127.0.0.1"

UDP_PORT = 2390
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP   
s.bind(('',UDP_PORT))  
while True:     
    data,addr=s.recvfrom(1024)
    data=str(data,"utf-8")
    print(data,addr[0])
    if addr[0]==UDP_TEST:   #'192.168.43.84'
        if data == "code_deb":
            received_codes=[]
        elif data == "code_fin":
            for code in list(codes): 
                if code not in received_codes:
                    del codes[code]
        else: 
            data=data.split(" ")
            id_velo = int(data[0])
            code = int(data[1])
            date_deb = data[2]+ " "+data[3]
            date_fin = data[4]+ " "+data[5]
            received_codes.append(code)
            if code not in codes:
                codes[code]=(id_velo,0,date_deb, date_fin)
    print(codes)
    if addr[0] == '192.168.43.129':
        try:
            code = int(data)
            print(code)
            print(codes)
            date = datetime.datetime.now().strftime('%Y-%m-%d %X')
            connection = sqlite3.connect('venv/Scripts/BDD_velos.db')
            cur = connection.cursor()
            if code in codes.keys():
                print(code, "accepted")
                print(codes[code][0])
                if codes[code][1] == 0:
                    print(codes[code][2])
                    s.sendto(bytes(str(codes[code][0]),'utf-8'),(UDP_IP,UDP_PORT))  #faire fonction
                    query = "UPDATE Historique SET date_recup = ? where id_velo = ? and date_deb = ?" 
                    cur.execute(query, (date, codes[code][0],codes[code][2]))
                    connection.commit()
                    codes[code]=(codes[code][0],1,codes[code][2])
                if codes[code][1] == 1: #faire fonction
                    query = "UPDATE Historique SET date_remise = ? where id_velo = ? and date_deb = ?"
                    print(codes[code])
                    cur.execute(query, (date, codes[code][0], codes[code][2]))
                    connection.commit()
                    print(codes)
            connection.close()
        except:
            None


    
    
