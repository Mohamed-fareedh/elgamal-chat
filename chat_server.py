import socket
import threading
import pickle
import ElGamal


# 接続済みクライアントは読み込みおよび書き込みを繰り返す
def loop_handler(connection, address, _pk, _sk):
    while True:
        try:
            res = ElGamal.decrypt(pickle.loads(connection.recv(4096)), pk, sk)  # デシリアライズ -> 復号
            for value in clients:
                if value[1][0] == address[0] and value[1][1] == address[1]:
                    print('Client({}, {}) : {}'.format(value[1][0], value[1][1], res))
                else:
                    value[0].send('Client({}, {}) : {}'.format(value[1][0], value[1][1], res).encode())
                    pass
        except Exception as e:
            print(e)
            break


if __name__ == '__main__':
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = '127.0.0.1'
    PORT = 55580
    socket.bind((HOST, PORT))
    socket.listen(5)  # 5 ユーザまで接続を許可
    clients = []
    while True:
        try:
            # 接続要求を受信
            conn, addr = socket.accept()
        except KeyboardInterrupt:
            socket.close()
            exit()
            break
        print('Client connected(IP:{}, PORT:{})'.format(addr[0], addr[1]))

        print('Key bits ?')
        bits = int(input('> '))
        print('OK, Your', str(bits)+'-bit keys are:')
        pk, sk = ElGamal.gen_key(bits=bits)
        print('public:', pk)  # 公開鍵
        print('secret:', sk)  # 秘密鍵
        line = str(pk[0])+' '+str(pk[1])+' '+str(pk[2])
        conn.send(line.encode())  # 公開鍵を送る
        print('Given the client the public key ...')

        clients.append((conn, addr))
        thread = threading.Thread(target=loop_handler, args=(conn, addr, pk, sk), daemon=True)
        thread.start()
