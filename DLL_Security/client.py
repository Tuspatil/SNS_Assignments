import numpy as np
import socket
import pickle

CIPHER_MATRIX = np.array([
    [-3, -3, -4],
    [0, 1, 1],
    [4, 3, 4]
])

CIPHER_MATRIX_INV = np.array([
    [1, 0, 1],
    [4, 4, 3],
    [-4, -3, -3]
])

ENCODING_RULE = lambda x : 27 if x == ' ' else ord(x)-ord('A')+1
DECODING_RULE = lambda x : ' ' if x == 27 else chr(x-1+ord('A'))
KEY = '1101'.lstrip('0')


def getp(data):
    if len(data) % 3 == 1:
        data += " "
    elif len(data) % 3 == 2:
        data += "  " 
    p = np.array(list(map(ENCODING_RULE, data))).reshape((3, len(data)//3), 'F')
    return p

def getRemainder(data):
    limit = len(data) - len(KEY) + 1
    data_list = list(data)

    for curpos in range(limit):
        if data_list[curpos] == '1':
            for i in range(len(KEY)):
                data_list[curpos+i] = '1' if KEY[i] != data_list[curpos+i] else '0'

    return ''.join(data_list)[limit:]


getCRC = lambda data : getRemainder("".join(list(map(lambda x : bin(ord(x))[2:], data))) + "0" * (len(KEY)-1))

def main():
    data = input()
    p = getp(data)
    EncData = np.dot(CIPHER_MATRIX, p)
    E = getCRC(data)

    msgBytes = pickle.dumps(EncData)
    EBytes = pickle.dumps(E)

    s = socket.socket()
    port = 5001
    s.connect(('127.0.0.1', port))

    s.send(msgBytes)
    s.send(EBytes)
    s.close()

if __name__ == '__main__':
    main()
