import socket
import threading
import pickle
import ElGamal


def Handler(_sock):
    while True:
        try:
            _recvline = _sock.recv(4096)
            print(_recvline.decode())
        except Exception as e:
            print(e)
            break

if __name__ == '__main__':
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = '127.0.0.1'
    PORT = 55580
    socket.connect((HOST, PORT))

    print('Waiting for input public key ...')
    pk_li = []
    while True:
        recvline = socket.recv(4096).decode()
        if recvline != '':
            pk_li = recvline.split(' ')
            pk = tuple([int(x) for x in pk_li])
            assert (len(pk) == 3)
            print('public key: ', pk)
            break

    while True:
        your_input = input('')
        socket.send(pickle.dumps(ElGamal.encrypt(your_input, pk)))  # 暗号化 -> シリアライズ
        thread = threading.Thread(target=Handler, args=(socket,), daemon=True)
        thread.start()
