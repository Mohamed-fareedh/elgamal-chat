import ElGamal
import pickle
import socket

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 8766

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((HOST, PORT))
    socket.listen(1)

    print('Waiting for connect from client ...')

    # コネクションとアドレスを取得
    connection, address = socket.accept()
    print('Client connected: ', address)

    print('Key bits ?')
    bits = int(input('> '))
    print('OK, Your', str(bits)+'-bit keys are:')
    pk, sk = ElGamal.gen_key(bits=bits)
    print('public:', pk)  # 公開鍵
    print('secret:', sk)  # 秘密鍵
    line = str(pk[0])+' '+str(pk[1])+' '+str(pk[2])
    connection.send(line.encode("UTF-8"))  # 公開鍵を送る
    print('Given the client the public key ...')
    data = connection.recv(4096).decode()  # クライアントからの応答を確認
    print('Client:', data)

    # 無限ループ　byeの入力でループを抜ける
    while True:

        # クライアントからデータを受信
        recvline = ElGamal.decrypt(pickle.loads(connection.recv(4096)), pk, sk)  # デシリアライズ -> 復号

        if recvline == 'bye':
            break
        else:
            print('Client:', recvline)

    # クローズ
    connection.close()
    socket.close()
    print('Server side closed.')
