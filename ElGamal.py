# coding: utf-8

# ElGamal暗号
# 参考：https://tex2e.github.io/blog/crypto/elgamal-encryption

# TODO 暗号文(タプルのリスト)をシリアライズして効率化する

from Crypto.Util import number


def gen_key(bits):
    """
    鍵生成
    :param bits: 鍵の長さ
    :return: 公開鍵: (p: 素数, g: Zp*の原始元, y: g^x(mod p)), 秘密鍵: x
    """
    # 素数p
    while True:
        q = number.getPrime(bits - 1)
        p = 2 * q + 1
        if number.isPrime(p):
            break
    # 原始元g
    while True:
        g = number.getRandomRange(3, p)
        # 原始元判定
        if pow(g, 2, p) == 1:
            continue
        if pow(g, q, p) == 1:
            continue
        break
    # 秘密値x
    x = number.getRandomRange(2, p - 1)
    # 公開値y
    y = pow(g, x, p)
    return (p, g, y), x


def encrypt(m, pk):
    """
    暗号化
    :param m: 平文 (str)
    :param pk: 公開鍵
    :return: 暗号文
    """
    p, g, y = pk
    c = []

    for one_str in list(m):  # 一文字ずつ切り出す
        _m = int.from_bytes(one_str.encode('UTF-8'), 'little')  # str(平文) -> Bytes -> int -> str
        assert (0 <= int(_m) < p)
        r = number.getRandomRange(2, p - 1)
        c1 = pow(g, r, p)
        c2 = (_m * pow(y, r, p)) % p
        c.append((c1, c2))
    return c


def decrypt(c, pk, sk):
    """
    復号
    :param c: 暗号文c1, c2のタプルのリスト
    :param pk: 公開鍵
    :param sk: 秘密鍵
    :return: 平文 (str)
    """
    p, g, y = pk
    d = ''

    for _c in c:
        c1, c2 = _c
        d += (c2 * pow(c1, p - 1 - sk, p) % p).to_bytes(3, 'little').decode().rstrip('\0')  # 復号＆ヌル文字削除
    return d


def main():

    pk, sk = gen_key(bits=512)
    print('pk:', pk)  # 公開鍵
    print('sk:', sk)  # 秘密鍵

    m = 'アンドロイドは電気羊の夢を見るか？'  # 平文
    print('m:', m)

    c = encrypt(m, pk)  # 暗号化
    print('c:', c)

    d = decrypt(c, pk, sk)  # 復号
    print('d:', d)


if __name__ == '__main__':
    main()
