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
timeout = 4 #sets the timeout

ACK_valid = 0

#now keep talking with the client
while 1:
    
    readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)
    for tempSocket in readable:
        # receive data from client (data, addr)
        d = s.recvfrom(1024)
        data = d[0]
        addr = d[1]
         
        if not data: #if there is no data we stop
            break
        
        if not ACK_valid: #statement will show how the problem is handled by the sender and receiver if there is an invalid checksum
            reply = 'ACK0: OK...' + data
            ACK_valid = 1
        else:
            reply = 'ACK1: OK...' + data
            ACK_valid = 0
         
        s.sendto(reply , addr)
        print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
     
s.close()