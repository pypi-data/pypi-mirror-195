import hashlib as _hashlib

class StringExtensions:
    def __init__(self, data: str):
        self.data = data

    def Hash(self, hashFunc=_hashlib.sha256()) -> str:
        hashFunc.update(self.data.encode())
        return hashFunc.hexdigest()
