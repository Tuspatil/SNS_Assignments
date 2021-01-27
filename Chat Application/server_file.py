import socket
import threading
import socketserver
import pickle
import os
from Crypto.Cipher import DES3
from random import randint
import sympy
from math import gcd

class Header:
    def __init__(self, opcode, source_addr, dest_addr):
        self.opcode = opcode
        self.source_addr = source_addr
        self.dest_addr = dest_addr

class PublicKey:
    def __init__(self, prime, root, pub_key):
        self.prime = prime
        self.root = root
        self.pub_key = pub_key

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

class Packet:
    def __init__(self, header, publicKey, reqServ, reqComp, encMsg, disconnect):
        self.header = header
        self.publicKey = publicKey
        self.reqServ = reqServ
        self.reqComp = reqComp
        self.encMsg = encMsg
        self.disconnect = disconnect



HEADER_LENGTH = 10
KEY_LENGTH = 24
SERVER_BUFFER_SIZE = 1024
CLIENT_BUFFER_SIZE = 1325
LOW_PRIME = 32768
HIGH_PRIME = 65536
CLIENT_HOME = "downloads/"
SERVER_HOME = "files/"

opcodeDict = {"PUBKEY":10, "REQSERV":20, "ENCMSG":30, "REQCOM":40, "DISCONNECT":50}



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


def primitive_root(modulo):
    required_set = set(num for num in range (1, modulo) if gcd(num, modulo) == 1)
    for g in range(1, modulo):
        actual_set = set(pow(g, powers, modulo) for powers in range (1, modulo))
        if required_set == actual_set:
            return g
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def getSharedKey(self):
        msg = self.request.recv(SERVER_BUFFER_SIZE)
        msgLen = int(msg[:HEADER_LENGTH])
        fullMsg = msg
        while len(fullMsg) < msgLen:
            msg = self.request.recv(SERVER_BUFFER_SIZE)
            fullMsg += msg
        msgFromClient = pickle.loads(fullMsg[HEADER_LENGTH:])
        serverPublicKey, secret = generatePublicKey(msgFromClient.publicKey)
        sharedKey = generateFullKey(msgFromClient.publicKey, secret)
        print(f"msgLength: {msgLen}, opcode: {msgFromClient.header.opcode}, prime: {msgFromClient.publicKey.prime}, root: {msgFromClient.publicKey.root}, publicKey: {msgFromClient.publicKey.pub_key}, secret: {secret}, \nShared Key: {sharedKey}")
        packet = Packet(Header(opcodeDict["PUBKEY"], socket.gethostname(), HOST), serverPublicKey, None, None, None, None) 
        msgToSend = pickle.dumps(packet)
        msgToSend = bytes(f"{len(msgToSend):<{HEADER_LENGTH}}", "ascii") + msgToSend
        self.request.sendall(msgToSend)
        print("Sent public key")
        return sharedKey

    def serveRequest(self, key):
        if len(key) < KEY_LENGTH:
            key = f"{key:<{KEY_LENGTH}}"
        msg = self.request.recv(SERVER_BUFFER_SIZE)
        msgLen = int(msg[:HEADER_LENGTH])
        fullMsg = msg
        while len(fullMsg) < msgLen:
            msg = self.request.recv(SERVER_BUFFER_SIZE)
            fullMsg += msg
        msgFromClient = pickle.loads(fullMsg[HEADER_LENGTH:])
        filename = msgFromClient.reqServ.filename
        print(f"Requested file: {filename} ", end = "")
        try:
            filepath = SERVER_HOME + filename
            with open(filepath, "rb") as file:
                fileInfo = os.stat(filepath)
                fileSize = fileInfo.st_size
                print(fileSize, "bytes.")
                data = file.read(SERVER_BUFFER_SIZE)
                cipher = DES3.new(key)
                while len(data) > 0 :
                    blockLength = len(data)
                    rem = blockLength % SERVER_BUFFER_SIZE
                    if rem:
                        data += bytes(SERVER_BUFFER_SIZE - rem)
                    encrypted_text = cipher.encrypt(data)
                    packet = Packet(Header(opcodeDict["ENCMSG"], socket.gethostname(), HOST), None, None, None, EncodedMsg(encrypted_text, blockLength), None) 
                    msgToSend = pickle.dumps(packet)
                    msgToSend = bytes(f"{len(msgToSend):<{HEADER_LENGTH}}", "ascii") + msgToSend
                    self.request.sendall(msgToSend)
                    data = file.read(SERVER_BUFFER_SIZE)
            packet = Packet(Header(opcodeDict["REQCOM"], socket.gethostname(), HOST), None, None, ReqComp(400), None, None) 
            msgToSend = pickle.dumps(packet)
            msgToSend = bytes(f"{len(msgToSend):<{HEADER_LENGTH}}", "ascii") + msgToSend
            self.request.sendall(msgToSend)
            print("File sent")
        except FileNotFoundError:
            print("File not found")
            packet = Packet(Header(opcodeDict["DISCONNECT"], socket.gethostname(), HOST), None, None, None, None, Disconnect()) 
            msgToSend = pickle.dumps(packet)
            msgToSend = bytes(f"{len(msgToSend):<{HEADER_LENGTH}}", "ascii") + msgToSend
            self.request.sendall(msgToSend)

    def handle(self):
        sharedKey1 = self.getSharedKey()
        sharedKey2 = self.getSharedKey()
        sharedKey3 = self.getSharedKey()
        print(f"shared keys:\n{sharedKey1}\n{sharedKey2}\n{sharedKey3}")
        self.serveRequest(str(sharedKey1) + str(sharedKey2) + str(sharedKey3))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):pass

HOST, PORT = "127.0.0.1", 9998
server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
print(f"Server started...")
server.serve_forever()
