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

ACKstatus = 0

test_var = 0

#now keep talking with the client
while 1:
    
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]
    
    checkSum = ip_checksum(data[1:-2])
    
    if not data: #if there is no data we stop
        break
    
    if (data[0] != str(ACKstatus)):
        print 'Duplicate detected.' #lets client know that there is a duplicate packet
        continue
    
    if (data != (str(ACKstatus) + data[1:-2] + checkSum)) and (data != (str(not ACKstatus) + data[1:-2] + checkSum)):
        print 'Corrupted packet!' #lets client know that there is a corrupted packet
        continue
    
    reply = str(ACKstatus)
    
    ACKstatus = 1 - ACKstatus
    
    if test_var == 1:
        time.sleep(12) #timeout period is delayed 
    test_var = test_var + 1
    
    s.sendto(reply , addr)

    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data[1:-2]
    
s.close()