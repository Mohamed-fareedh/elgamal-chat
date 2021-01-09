# 参考 : https://itsakura.com/python-socket

import socket
import pickle
import ElGamal

if __name__ == '__main__':
    IP = '127.0.0.1'
    PORT = 8766
    SERVER = (IP, PORT)

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect(SERVER)

    print('Waiting for input public key ...')
    recvline = ''
    sendline = ''
    pk_li = []
    while True:
        recvline = socket.recv(4096).decode()
        if recvline != '':
            pk_li = recvline.split(' ')
            pk = tuple([int(x) for x in pk_li])
            assert (len(pk) == 3)
            print('public key: ', pk)
            socket.send('OK!'.encode('UTF-8'))
            break

    line = ''
    while line != 'bye':
        # 標準入力からデータを取得
        print('Enter your message here.')
        line = input('> ')

        # サーバに送信
        socket.send(pickle.dumps(ElGamal.encrypt(line, pk)))  # 暗号化 -> シリアライズ

    socket.close()

    print('Client side closed.')
