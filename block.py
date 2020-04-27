import time
import utils
from pow import PoW
import pickle
from merkle_tree import MerkleTree
import binascii

class Block():
    def __init__(self, tx_lst, height, prev_block_hash='', bits=16):
        self._time = utils.encode(str(int(time.time())))
        self._tx_lst = tx_lst
        self.bits = bits
        self._height = height
        self._prev_block_hash = utils.encode(prev_block_hash)
        self._nonce = None
        self._hash = None

    def proof_of_block(self):
        pow = PoW(self)
        nonce, hash = pow.run()
        self._nonce, self._hash = nonce, utils.encode(hash)
        return self

    def hash_transactions(self):
        tx_byte_lst = []
        for tx in self._tx_lst:
            tx_byte_lst.append(tx.to_bytes())

        m_tree = MerkleTree(tx_byte_lst)

        return utils.decode(binascii.hexlify(m_tree.root_hash))

    def serialize(self):
        # serializes the block
        return pickle.dumps(self)

    def deserialize(self, data):
        return pickle.load(data)

    @property
    def height(self):
        return self._height

    @property
    def prev_block_hash(self):
        return utils.decode(self._prev_block_hash)

    @property
    def nonce(self):
        return self._nonce

    @property
    def hash(self):
        return utils.decode(self._hash)

    @property
    def time(self):
        return str(self._time)

    @property
    def transactions(self):
        return self._tx_lst
