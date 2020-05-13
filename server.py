import socket
import sys
from thread import *

HOST = '127.0.0.1'	# Symbolic name meaning all available interfaces
PORT = 2589	# Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

myList = []

#Bind socket to local host and port
try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
	
print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'

#Function for handling connections. This will be used to create threads
def clientthread(conn):
	#Sending message to connected client
	conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
	
	#infinite loop so that function do not terminate and thread do not end.
	while True:
		
		#Receiving from client
        if 'q!' in conn.recv(1024):
            s.close()
		data = conn.recv(1024)
        
		reply = 'OK...' + data

		if not data: 
			break
	
		conn.sendall(reply)

        if '!sendall' in conn.recv(1024):
            for member in myList:
                member.sendall(reply)
	
	#came out of loop
	conn.close()

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
	conn, addr = s.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])

    myList.append(addr)
	
	#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
	start_new_thread(clientthread ,(conn,))

s.close()