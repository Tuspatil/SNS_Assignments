from random import randint
from math import gcd
import sympy
import socket
import os
import getpass
import pickle
import sys
from Crypto.Cipher import DES3

HEADER_LENGTH = 10
KEY_LENGTH = 24
SERVER_BUFFER_SIZE = 1024
CLIENT_BUFFER_SIZE = 1325
LOW_PRIME = 32768
HIGH_PRIME = 65536
CLIENT_HOME = "downloads/"
SERVER_HOME = "files/"

opcodeDict = {"PUBKEY":10, "REQSERV":20, "ENCMSG":30, "REQCOM":40, "DISCONNECT":50}

class PublicKey:
    def __init__(self, prime, root, pub_key):
        self.prime = prime
        self.root = root
        self.pub_key = pub_key

class Header:
    def __init__(self, opcode, source_addr, dest_addr):
        self.opcode = opcode
        self.source_addr = source_addr
        self.dest_addr = dest_addr

class Packet:
    def __init__(self, header, publicKey, reqServ, reqComp, encMsg, disconnect):
        self.header = header
        self.publicKey = publicKey
        self.reqServ = reqServ
        self.reqComp = reqComp
        self.encMsg = encMsg
        self.disconnect = disconnect


def primitive_root(modulo):
    required_set = set(num for num in range (1, modulo) if gcd(num, modulo) == 1)
    for g in range(1, modulo):
        actual_set = set(pow(g, powers, modulo) for powers in range (1, modulo))
        if required_set == actual_set:
            return g



def generatePublicKey(publicKey = None):
    if publicKey == None:
        primeNo = sympy.randprime(LOW_PRIME, HIGH_PRIME)
        primitiveRoot = primitive_root(primeNo)
        publicKey = PublicKey(primeNo, primitiveRoot, None)
    secret = randint(1, publicKey.prime)
    return PublicKey(publicKey.prime, publicKey.root, pow(publicKey.root, secret, publicKey.prime)), secret


def generateFullKey(publicKey, secret):
    fullKey = pow(publicKey.pub_key, secret, publicKey.prime)
    return fullKey

class ReqServ:
    def __init__(self, filename):
        self.filename = filename

class ReqComp:
    def __init__(self, status):
        self.status = status

class EncodedMsg:
    def __init__(self, msg, length):
        self.msg = msg
        self.length = length

class Disconnect:
    def __init__(self):
        self.disconnectMsg = "See you soon!"

def key_establishment(host,port=9998):
	# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# sock.connect(host)
# -------Establishing the first key--------------
	generatedKey1,secret1=generatePublicKey()
	packet1 = Packet(Header(opcodeDict["PUBKEY"], socket.gethostname(), HOST), generatedKey1, None, None, None, None)
	msgToSend1 = pickle.dumps(packet1)
	msgToSend1 = bytes(f"{len(msgToSend1):<{HEADER_LENGTH}}", "ascii") + msgToSend1
	sock.sendall(msgToSend1)

	msg1 = sock.recv(CLIENT_BUFFER_SIZE)
	msgLen1 = int(msg1[:HEADER_LENGTH])
	fullMsg1 = msg1
	while len(fullMsg1) < msgLen1:
	    msg1 = self.request.recv(CLIENT_BUFFER_SIZE)
	    fullMsg1 += msg1
	msgFromServer1 = pickle.loads(fullMsg1[HEADER_LENGTH:])
	print(f"Recieved:\nOpcode: {msgFromServer1.header.opcode}, Prime: {msgFromServer1.publicKey.prime}, Root: {msgFromServer1.publicKey.root}, PubKey: {msgFromServer1.publicKey.pub_key}")
	sharedKey1 = generateFullKey(msgFromServer1.publicKey, secret1)

# -------Establishing the second key--------------
	
	generatedKey2,secret2=generatePublicKey()
	packet2 = Packet(Header(opcodeDict["PUBKEY"], socket.gethostname(), HOST), generatedKey2, None, None, None, None)
	msgToSend2 = pickle.dumps(packet2)
	msgToSend2 = bytes(f"{len(msgToSend2):<{HEADER_LENGTH}}", "ascii") + msgToSend2

	sock.sendall(msgToSend2)

	msg2 = sock.recv(CLIENT_BUFFER_SIZE)
	msgLen2 = int(msg2[:HEADER_LENGTH])
	fullMsg2 = msg2
	while len(fullMsg2) < msgLen2:
	    msg2 = self.request.recv(CLIENT_BUFFER_SIZE)
	    fullMsg2 += msg2
	msgFromServer2 = pickle.loads(fullMsg2[HEADER_LENGTH:])
	print(f"Recieved:\nOpcode: {msgFromServer2.header.opcode}, Prime: {msgFromServer2.publicKey.prime}, Root: {msgFromServer2.publicKey.root}, PubKey: {msgFromServer2.publicKey.pub_key}")
	sharedKey2 = generateFullKey(msgFromServer2.publicKey, secret2)


# -------Establishing the third key--------------
	
	generatedKey3,secret3=generatePublicKey()
	packet3 = Packet(Header(opcodeDict["PUBKEY"], socket.gethostname(), HOST), generatedKey3, None, None, None, None)
	msgToSend3 = pickle.dumps(packet3)
	msgToSend3 = bytes(f"{len(msgToSend3):<{HEADER_LENGTH}}", "ascii") + msgToSend3

	sock.sendall(msgToSend3)

	msg3 = sock.recv(CLIENT_BUFFER_SIZE)
	msgLen3 = int(msg3[:HEADER_LENGTH])
	fullMsg3 = msg3
	while len(fullMsg3) < msgLen3:
	    msg3 = self.request.recv(CLIENT_BUFFER_SIZE)
	    fullMsg3 += msg3
	msgFromServer3 = pickle.loads(fullMsg3[HEADER_LENGTH:])
	print(f"Recieved:\nOpcode: {msgFromServer3.header.opcode}, Prime: {msgFromServer2.publicKey.prime}, Root: {msgFromServer2.publicKey.root}, PubKey: {msgFromServer2.publicKey.pub_key}")
	sharedKey3 = generateFullKey(msgFromServer3.publicKey, secret3)
	return sharedKey1,sharedKey2,sharedKey3


def encrypt_file(host,filename):
	sharedKey1,sharedKey2,sharedKey3=key_establishment(host,9998)
	print(f"Shared keys: {sharedKey1}\n{sharedKey2}\n{sharedKey3}")
	# ----------from main file----------
	# print("Enter filename:")
	# filename = input()
	# ----------------------------------

	# --------------sendFileReq(filename)------
	packet1 = Packet(Header(opcodeDict["REQSERV"], socket.gethostname(), HOST), None, ReqServ(filename), None, None, None)
	msgToSend1 = pickle.dumps(packet1)
	msgToSend1 = bytes(f"{len(msgToSend1):<{HEADER_LENGTH}}", "ascii") + msgToSend1
	sock.sendall(msgToSend1)    
	# -------------------------------------------

	# --------------getResponse(str(sharedKey1) + str(sharedKey2) + str(sharedKey3), filename)------
	key1=str(sharedKey1) + str(sharedKey2) + str(sharedKey3)
	msg1 = sock.recv(CLIENT_BUFFER_SIZE)
	msgLen1 = int(msg1[:HEADER_LENGTH])
	fullMsg1 = msg1
	while len(fullMsg1) < msgLen1:
	    msg1 = sock.recv(CLIENT_BUFFER_SIZE)
	    fullMsg1 += msg1
	# msgFromServer = pickle.loads(fullMsg[utils.HEADER_LENGTH:])
	msgFromServer1 = pickle.loads(fullMsg1[HEADER_LENGTH:HEADER_LENGTH + msgLen1])
	if msgFromServer1.header.opcode == opcodeDict["DISCONNECT"]:
	    print("File not found at server")
	    return
	if len(key1) < KEY_LENGTH:
	    key1 = f"{key1:<{KEY_LENGTH}}"
	cipher = DES3.new(key1)
	with open(CLIENT_HOME + filename, "wb") as file:
	    while msgFromServer1.header.opcode != opcodeDict["REQCOM"]:
	        decrypted_data = cipher.decrypt(msgFromServer1.encMsg.msg)
	        file.write((decrypted_data)[:msgFromServer1.encMsg.length])
	        msg1 = fullMsg1[HEADER_LENGTH + msgLen1:] + sock.recv(CLIENT_BUFFER_SIZE)
	        #msg = sock.recv(utils.CLIENT_BUFFER_SIZE)
	        msgLen1 = int(msg1[:HEADER_LENGTH])
	        fullMsg1 = msg1
	        while len(fullMsg1) < msgLen1:
	            msg1 = sock.recv(CLIENT_BUFFER_SIZE)
	            fullMsg1 += msg1
	        # msgFromServer = pickle.loads(fullMsg[utils.HEADER_LENGTH:])
	        msgFromServer1 = pickle.loads(fullMsg1[HEADER_LENGTH:HEADER_LENGTH + msgLen1])
	print("file saved")


	# ------------------------------------------
	sock.shutdown(socket.SHUT_RDWR)
	getpass.getpass(prompt="")	


def sendFile(filename,host):
	encrypt_file(host,filename)

HOST, PORT = sys.argv[1], 9998
print("")
while True:
	os.system("clear")
	print("Key exchange initiated...")
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((HOST, PORT))
	# host=sys.argv[1]
	print("Enter filename:")
	filename = input()
	sendFile(filename,HOST)