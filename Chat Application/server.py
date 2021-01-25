import socket             

connInfo = {}
authInfo = {}

def init():  
	userFile = open('users.txt', 'r+') 
	users = userFile.readlines()
	for user in users:
		temp = user.split('#')
		authInfo[temp[0]]=temp[1]
def signUp(uname,psswd,s):
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
	print(authInfo)
	if(authInfo[uname] == psswd):
		msg = "valid"
		s.send(msg.encode('ascii'))
		connInfo[uname]=port
	else:
		msg = "invalid"
		s.send(msg.encode('ascii'))
	s.close()	

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
		for key in authInfo:
			msg = msg+key+"#"
		data = msg.encode('ascii')
		c.send(data)
		c.close()
	elif(param[0] == "getPort"):
		msg = str(connInfo[param[1]])
		c.send(msg.encode('ascii'))
		c.close()			

  
# Close the connection with the client  
c.close()