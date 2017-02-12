#!/usr/bin/python
# -*- coding: utf-8 -*-
import serial
import time
import socket
import sqlite3
import os
from datetime import datetime

conn = sqlite3.connect("Sensor.db") # or use :memory: to put it in RAM

cursor = conn.cursor()
sql_file = os.path.join(os.path.dirname(__file__), 'Sensor.db')
needs_creation = not os.path.exists(sql_file) 
db_connection = sqlite3.connect(sql_file)
db_connection.row_factory = sqlite3.Row

# create a table
if needs_creation:
    print 'Creating initial database...'
    cursor = db_connection.cursor()

    db_connection.commit()
    print 'Database created.'
conn.row_factory = sqlite3.Row;
cursor.executescript("""
                   CREATE TABLE IF NOT EXISTS Sensor (
[ID] varchar(50),
[YEAR] varchar(50),
[MONTH] varchar(50),
[DAY] varchar(50),
[HOUR] varchar(50),
[GPS_MIN] varchar(50),
[GPS_SEC] varchar(50),
[SPEED] varchar(50),
[GPS_ALT] varchar(50),
[TEMP] varchar(50),
[GYRO_X] varchar(50),
[GYRO_Y] varchar(50),
[GYRO_Z] varchar(50),
[ACC_X] varchar(50),
[ACC_Y] varchar(50),
[ACC_Z] varchar(50),
[GRAV_X] varchar(50),
[GRAV_Y] varchar(50),
[GRAV_Z] varchar(50)
 )""" )
#db_connection.commit()
conn.commit()


UDP_Stream_IP = "192.168.0.71"
UDP_Stream_PORT = 5001

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("192.168.0.52",5005))
sock.sendto(UDP_Stream_IP, UDP_Stream_PORT)

while True:
    data, addr = sock.recvfrom(65536)
    #time.sleep(2)
    print "received message:", data
    DataLength = len(data) - 1
    output = str(data[0:DataLength]) + '\n'
    #time.sleep(0.5)
    line = output.rstrip().split(',')
    #line = line.strip(',')
    line = filter(None,line)

    try:
        
    cursor.execute("""INSERT OR IGNORE INTO Sensor (ID, YEAR, MONTH, DAY, HOUR, GPS_MIN, GPS_SEC, SPEED, GPS_ALT, TEMP, GYRO_X, GYRO_Y, GYRO_Z, ACC_X, ACC_Y, ACC_Z, GRAV_X, GRAV_Y, GRAV_Z) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],line[8],line[9],line[10],line[11],line[12],line[13],line[14],line[15],line[16],line[17],line[18]))

    conn.commit()
    except:
         print "failed to insert data"
    finally:
        cursor.close()  #close just incase it failed    
    allentries = []
    cursor.execute('SELECT * FROM Sensor limit 1')
    # Count No of Entries into Database
    cursor.execute("SELECT Count(*) FROM Sensor")

    allentries=cursor.fetchall()
    # Print All Entries
    print allentries
        
        

