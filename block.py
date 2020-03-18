import time


class Block():
    def __init__(self, prevHash):
        self.transaction
        self.time = 0
        self.bits = 0
        self.height
        self._nonce
        self._prevBlockHash = prevHash
        self._hash

    def setHash(self):
        raise NotImplementedError
