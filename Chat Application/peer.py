# import socket programming library 
import socket 
import sys

from _thread import *
import threading 

print_lock = threading.Lock() 
 
def threaded(s): # for accepting msgs

	while True: 
		c, addr = s.accept()
		data = c.recv(1024) 
		print(str(data.decode('ascii')))
		c.close() 


def Main(): 
	host = ""  
	#port = 12345
	port = int(sys.argv[1])
	print("Are you an existing user?")
	choice = input() #yes/no
	if(choice == "no"):
		print("Enter your username")
		uname = input()
		print("Enter your password")
		psswd = input()
		print("Re-enter your password")
		psswd1 = input()
		if(psswd != psswd1):
			exit()
		data = "up#"+uname+"#"+psswd 
		serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		serverPort = 8080
		serverSocket.connect((host,serverPort))
		serverSocket.send(data.encode('ascii')) #At server side just write this into authentication file
		response = serverSocket.recv(1024)
		ack = response.decode('ascii')
		if(ack == "exist"):
			print("User with this username already exist. Please select other username")
		else:
			print(ack)	
		serverSocket.close()

	print("Sign in to continue")
	print("Enter username:")
	uname = input()
	print("Enter password:")
	passwd = input()
	data = "in#"+uname+"#"+passwd+"#"+str(port)
	serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	serverPort = 8080
	serverSocket.connect((host,serverPort))
	serverSocket.send(data.encode('ascii')) #At server side check for authentication
	response = serverSocket.recv(1024)
	ack = response.decode('ascii')
	if(ack == "invalid"):
		print("Invalid credentials. Exiting.....")
		exit()
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket

	s.bind((host, port)) # command line arguments
 
	s.listen(5) #listening on the port

	start_new_thread(threaded, (s,))

	print("peer is listening as well as sending")
		

	while True: #Act like sender here onwards have to connect to other client which is acting as server
		#server stuff will be involved of fetching port of user based on name
		#1. signup/sign in [Done]
		#2. connecting to server to validate the user.[Done]
		#3. show online users -> send CLIENTNAME msg -> get port of client -> send the msg
		print("User: "+uname)
		print("1.Show online users\n2.Send text\n4.Create Group\n5.Join Group\n6.List Groups\n7.Send to Group")
		choice = int(input())
		if(choice == 1):
			clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			msg = "ping#uname"
			clientSocket.connect((host,8080))
			clientSocket.send(msg.encode('ascii'))
			response = clientSocket.recv(1024)
			clients = response.decode('ascii')
			clientList = clients.split('#')
			print(clientList)
			clientSocket.close()
		elif(choice == 2):
			serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			serverSocket.connect((host,8080))
			print("Whom do u wanna send from available users")
			receiver = input() #Taking input to whom we wanna connect
			msg = "getPort#"+receiver 
			serverSocket.send(msg.encode('ascii'))
			temp = serverSocket.recv(1024)
			senderPort = int(temp.decode('ascii'))
			serverSocket.close()
			print(senderPort)
			clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			clientSocket.connect((host,senderPort))
			print("Type your message:")
			msg = input()
			clientSocket.send(msg.encode('ascii'))
			clientSocket.close()
		elif(choice == 4):
			print("Enter the name of the group")
			groupName = input()
			msg = "cg#"+groupName+"#"+str(port)
			serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			serverSocket.connect((host,8080))
			serverSocket.send(msg.encode('ascii'))
			ack = serverSocket.recv(1024)
			ackData = ack.decode('ascii')
			print(ackData)
			serverSocket.close()
		elif(choice == 5): #Join Group
			print("Enter the group name you wanna join")
			groupName = input()
			msg = "jg#"+groupName+"#"+str(port)
			serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			serverSocket.connect((host,8080))
			serverSocket.send(msg.encode('ascii'))
		elif(choice == 6 ): #List Groups
			msg = "list#"
			serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			serverSocket.connect((host,8080))
			serverSocket.send(msg.encode('ascii'))
			groupInfo = serverSocket.recv(1024)
			groupList = groupInfo.decode('ascii')
			groupDetails = groupList.split('#')
			print(groupDetails)
		elif(choice == 7):
			print("Enter group message")
			grpmsg = input()
			msg = "sg#"+str(port)
			serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			serverSocket.connect((host,8080))
			serverSocket.send(msg.encode('ascii'))
			temp = serverSocket.recv(1024) #Got all the groups which current user is part of
			serverSocket.close()
			groupNames = temp.decode('ascii')
			groupDetails = groupNames.split('#')
			print(groupDetails)
			for groupName in groupDetails: #now we have all groups in which current user belong. Now we have to get all peer belonging to that group
				msg = "getUsers#"+groupName
				serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				serverSocket.connect((host,8080))
				serverSocket.send(msg.encode('ascii'))
				userlist = serverSocket.recv(1024)
				userList = userlist.decode('ascii') #got the string
				users = userList.split('#') # we have all ports where message is to be sent
				print(users)
				for user in users:
					port = int(user)
					clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
					clientSocket.connect((host,port))
					clientSocket.send(grpmsg.encode('ascii'))
					clientSocket.close()



if __name__ == '__main__': 
	Main() 
