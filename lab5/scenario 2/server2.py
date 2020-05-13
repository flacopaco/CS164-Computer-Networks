#'''
#    Simple udp socket server
#'''

import socket
import sys
import time
import random
import select
from socket import timeout
from check import ip_checksum
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port
 
# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
 
# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

inputs = [s]
outputs = [ ]
timeout = 4

ACKstatus = 0

#now keep talking with the client
while 1:
    
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]
    
    checkSum = ip_checksum(data[1:-2])
    
    if not data: #if there is no data we stop
        break
    
    if (data != (str(ACKstatus) + data[1:-2] + checkSum)) and (data != (str(not ACKstatus) + data[1:-2] + checkSum)): #checksum comparison
        print 'Corrupted packet!' #this will let the client know that there has been a corrupted packet
        continue
    
    response = str(ACKstatus)
    
    ACKstatus = 1 - ACKstatus
    
    s.sendto(response , addr)
    
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data[1:-2]
    
s.close()