import socket             

connInfo = {}
authInfo = {}
groupToUsers = {} #groupname to ports to send msgs [Giving members of the group]
userToGroups = {} #port to groupname for membership purpose[to send msg to all groups which he is part of]

def createGroup(groupName,port,s):
	lst1 = []
	lst1.append(port)
	groupToUsers[groupName]=lst1
	if port in userToGroups.keys():
		lst=userToGroups[port]
		lst.append(groupName)
	else:
		lst= []
		lst.append(groupName)
	userToGroups[port] = lst
	msg = "Group successfully created"
	s.send(msg.encode('ascii'))
	s.close()
	print(connInfo)
	print(authInfo)
	print(groupToUsers)
	print(userToGroups)

def init():  
	userFile = open('users.txt', 'r+') 
	users = userFile.readlines()
	for user in users:
		temp = user.split('#')
		authInfo[temp[0]]=temp[1].strip('\n')

def signUp(uname,psswd,s):
	print(connInfo)
	print(authInfo)
	print(groupToUsers)
	print(userToGroups)
	if uname in authInfo.keys():
		msg = "exist"
		s.send(msg.encode('ascii'))
		s.close()
	else:	
		authInfo[uname]=psswd
		fp = open('users.txt','a+')
		fp.write(uname+"#"+psswd+"\n")
		fp.close()
		msg = "Sign up successfull, please sign in to continue"
		s.send(msg.encode('ascii'))
		s.close()

def signIn(uname,psswd,port,s):
	print(connInfo)
	print(authInfo)
	print(groupToUsers)
	print(userToGroups)
	if(authInfo[uname] == psswd):
		msg = "valid"
		s.send(msg.encode('ascii'))
		connInfo[uname]=port
	else:
		msg = "invalid"
		s.send(msg.encode('ascii'))
	s.close()

def joinGroup(groupName,port,s):
	print(connInfo)
	print(authInfo)
	print(groupToUsers)
	print(userToGroups)
	values = groupToUsers[groupName] #Entering port corresponding to the groupname (KeyError not possible according to assumptions)
	values.append(port)
	groupToUsers[groupName]=values
	
	if port in userToGroups.keys():
		users = userToGroups[port]
		users.append(groupName)
		userToGroups[port] = users
	else:
		lst = []
		lst.append(groupName)
		userToGroups[port] = lst	
	msg = "You have been added to group\n"
	s.send(msg.encode('ascii'))

s = socket.socket()       
print ("Socket successfully created")   
port = 8080                
s.bind(('', port))        
print ("socket binded to %s" %(port))  
  
# put the socket into listening mode  
s.listen(5)   
print ("socket is listening")            
init() 
while True:  
  
	# Establish connection with client.  
	c, addr = s.accept()       
	data = c.recv(1024)
	msg = data.decode('ascii')
	param = msg.split('#')
	if(param[0] == "up"):
		signUp(param[1],param[2],c)
	elif(param[0] == "in"):
		port = int(param[3])
		signIn(param[1],param[2],port,c)
	elif(param[0] == "ping"):
		msg = ""
		for key in connInfo:
			msg = msg+key+"#"
		msg = msg[:-1]	
		data = msg.encode('ascii')
		c.send(data)
		c.close()
	elif(param[0] == "getPort"):
		msg = str(connInfo[param[1]])
		c.send(msg.encode('ascii'))
		c.close()
	elif(param[0] == "cg"):
		createGroup(param[1],int(param[2]),c);
	elif(param[0] == "jg"):
		joinGroup(param[1],int(param[2]),c)
	elif(param[0] == "list"):
		lst = groupToUsers.keys()
		msg=""
		for group in lst:
			msg = msg+group+"#"
		msg = msg[:-1]	
		c.send(msg.encode('ascii'))
		c.close()
	elif(param[0] == "sg"):
		port = int(param[1])
		groupNames = userToGroups[port] #given the port number, it will return groups
		print("server side->GroupNames: ",groupNames)
		msg = ""
		for grp in groupNames:
			msg = msg+grp+"#"
		msg1=msg[:-1]
		print("Printing message on server side ", msg1)
		c.send(msg1.encode('ascii'))
		c.close()
	elif(param[0] == "getUsers"):
		print("Printing name of the group: ",param[1])
		userlist = groupToUsers[param[1]]
		msg = ""
		for user in userlist:
			msg = msg+str(user)+"#"
		msg1=msg[:-1]
		c.send(msg1.encode('ascii'))
		c.close()		
# Close the connection with the client  
c.close()