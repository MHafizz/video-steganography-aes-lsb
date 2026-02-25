# crypto_aes.py
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class AESCipher:
    def __init__(self, password: str):
        self.password = password

    def _derive_key(self, salt: bytes):
        return PBKDF2(self.password.encode('utf-8'), salt, dkLen=32, count=1_000_000)

    def encrypt(self, data: bytes) -> bytes:
        salt = get_random_bytes(16)
        iv = get_random_bytes(16)
        key = self._derive_key(salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct = cipher.encrypt(pad(data, AES.block_size))
        return salt + iv + ct

    def decrypt(self, enc_data: bytes) -> bytes:
        salt = enc_data[:16]
        iv = enc_data[16:32]
        key = self._derive_key(salt)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct = enc_data[32:]
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt
