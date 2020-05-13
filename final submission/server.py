#Samuel Liu SID: 861270589
#CS164 Mininet Topology Project
#implemented up to part 3

import socket
import json

from thread import * #threading used to handle new connections

HOST = '10.0.0.4'
PORT = 4090

def server_side(conn):
	try:
		conn.send('Please Enter Your Username: ') #prompts user to input username
		usr = conn.recv(1024)
		conn.send('Please Enter Your Password: ') #prompts user to input password
		pwd = conn.recv(1024)

		if usr not in clients or clients[usr]['password'] != pwd:
			conn.send('Username or Password is invalid.\n')
			conn.close()
		
		clients[usr]['active_status'] = True; #sets user to online
		clients[usr]['connection'] = conn; #sets user as connected
		
		menu = """
		What would you like to do? 
		1. Send a Private Message 
		2. Send a Broadcast Message  
		3. View Unread Messages
        4. Change Your Password
		5. Logout
		"""

		conn.send(menu + "\n\n")
		conn.send('You have {} unread messages\n'.format(len(clients[usr]['inbox'])))

		while 1:
			data = conn.recv(1024)
			if not data: #checks if client uses correct data
				conn.send('Please try again.')
				continue
			
			if data == '1': #allows client to send a private message
				conn.send('Please enter a user to send a message to: ')
				target = conn.recv(1024) #target must be an existing user (hardcoded in)
				conn.send('Enter your Message: ')
				msg = conn.recv(1024)
				msg = msg + '\n'
			
				if clients[target]['active_status']:
					conn.send('Message has been sent.\n\n')
					clients[target]['connection'].send('{}: {}'.format(usr, msg))
					clients[target]['connection'].send(menu)
				else:
					conn.send('User is offline. Message will still be sent.\n\n') #if user is not online
					clients[target]['inbox'].append({'from': usr, 'message': msg})

			if data == '2': #broadcast message
				conn.send('Message: ')
				msg = conn.recv(1024)
				msg = msg + '\n'
				
                for usrs in clients:
					if clients[usrs]['active_status']:
						clients[usrs]['connection'].send('{}: {}'.format(usr, msg))
						clients[usrs]['connection'].send(menu)
				conn.send('Broadcast Message Sent.')
			
			if data == '3': #view unread messages
				for message in clients[usr]['inbox']:
					conn.send('{}: {}'.format(message['from'], message['message']))
				del clients[usr]['inbox'][:] #removes the number for viewcount
			
			
			if data == '4': #allows client to change password
				conn.send('Please enter your old password: ')
				oldPass = conn.recv(1024)
				conn.send('Please enter a new password: ')
				newPass = conn.recv(1024)
				
				if oldPass == clients[usr]['password']:
					clients[usr]['password'] = newPass
					conn.send('Password has been changed.\n')
				else:
					conn.send('Password change failed. Please re-enter.')

			if data == '5': #client logout function
				clients[usr]['active_status'] = False #changes status of the user to offline
				conn.send('Log out successful. \n')
				conn.close()
		
			conn.send('\n\n' + menu + "\n\n")
			conn.send('{} unread messages\n'.format(len(clients[usr]['inbox'])))
	except:
		print('Client has been disconnected from the server.')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #from lab 4 
s.bind((HOST, PORT))
s.listen(10)

print('Waiting for clients:{}'.format(PORT))

while 1:
	conn, addr = s.accept()
	print('Connected with {}:{}'.format(addr[0], addr[1]))
	start_new_thread(server_side, (conn,)) #vital for multiple client connections. 

s.close()

clients = { #hardcode of username and password
	'user1': {
		'password': 'user1',
		'active_status': False,
		'connection': None,
		'inbox': [],
	}, 
	'user2': {
		'password': 'user2',
		'active_status': False,
		'connection': None,
		'inbox': [],
	},
	'user3': {
		'password': 'user3',
		'active_status': False,
		'connection': None,
        'inbox': [],
	} 
}