import base64
from Crypto.Cipher import AES
from Crypto import Random

BS = 16
Pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode("utf-8")
Unpad = lambda s: s[:-ord(s[len(s) - 1:])].decode("utf-8")

class AESCipher:
    def __init__(self, key):
        self.key = key

    def Encrypt(self, raw):
        raw = Pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def Decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return Unpad(cipher.decrypt(enc[16:]))


