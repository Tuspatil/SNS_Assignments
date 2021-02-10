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

def decryptp(dataMarix):
    p = np.dot(CIPHER_MATRIX_INV, dataMarix)
    p = np.reshape(p, (p.shape[0] * p.shape[1]), 'F')
    return "".join(list(map(DECODING_RULE, p))).strip() #typecast p to a python list


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

    s = socket.socket()
    port = 5001
    s.bind(('', port))
    s.listen(2)

    c, addr = s.accept()
    data = c.recv(1024000)
    data1 = data[:data[1:].find(b'\x80')]
    data1 += b'.'

    data2 = data[data[1:].find(b'\x80'):]
    data2 = data2[1:]

    EncData = pickle.loads(data1)
    E = pickle.loads(data2)

    recText = decryptp(EncData)
    print('The received text is: ', end='')
    print(recText)

    if getCRC(recText) == E:
        print('String is Correct')
    else:
        print('String is Incorrect')
    c.close()
    s.close()


if __name__ == '__main__':
    main()
