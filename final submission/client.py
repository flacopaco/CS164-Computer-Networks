#Samuel Liu SID: 861270589
#CS164 Mininet Topology Project
#implemented up to part 3

from __future__ import print_function #Python 3.0 print function

import socket
import json
import getpass #used for asking user for password until they press return
from threading import Timer

HOST = '10.0.0.4'
PORT = 4090

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while 1: 
	d, addr = s.recvfrom(1024)
	print(d, end='') #stops client from infinte input
	inpt = ''
	
    if 'Password' in d and 'Menu' not in d:
		inpt = getpass.getpass('')
	else:
		inpt = raw_input()

	s.send(inpt)

s.close()