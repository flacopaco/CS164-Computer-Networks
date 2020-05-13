#'''
#    udp socket client
#'''

import socket   #for sockets
import sys  #for exit
import time
import random
import select
from socket import timeout
from check import ip_checksum

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
 
host = 'localhost';
port = 8888;

packet_status = 0

while(1) :
    msg = raw_input('Enter message to send : ')
    
    checksum = ip_checksum(msg) # computes the checksum of the message
    
    try :
        #Set the whole string
        s.sendto(str(packet_status) + msg + checksum, (host, port))
        
        s.settimeout(10) #this will set the timer for the timeout scenario
        
        try:
            # receive data from client (data, addr)
            d = s.recvfrom(1024)
            reply = d[0]
            addr = d[1]
        
        except socket.timeout:
            print 'Re-sending...' #will let the client know the packet is resending 
            checksum = ip_checksum(msg)
            
            s.sendto(str(packet_status) + msg + checksum, (host, port))
            
            d = s.recvfrom(1024)
            reply = d[0]
            addr = d[1]
        
        print 'Server reply : ' + reply
        
        packet_status = 1 - packet_status
        
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()