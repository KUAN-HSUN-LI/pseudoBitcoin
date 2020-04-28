import hashlib
import sys

import utils


class PoW():
    max_nonce = sys.maxsize

    def __init__(self, block):
        self._block = block
        self._target = 1 << (256 - block.bits)

    def _prepare_data(self, nonce):
        data_lst = [self._block.prev_block_hash,
                    self._block.hash_transactions(),
                    self._block.time,
                    str(self._target),
                    str(nonce)]
        return utils.encode(''.join(data_lst))

    def validate(self):
        data = self._prepare_data(self._block.nonce)
        hash_hex = utils.sum256_hex(data)
        hash_int = int(hash_hex, 16)

        return True if hash_int < self._target else False

    def run(self):
        nonce = 0

        print(f"Mining the block {self._block.height}\n")

        while nonce < self.max_nonce:
            data = self._prepare_data(nonce)
            hash_hex = utils.sum256_hex(data)
            hash_int = int(hash_hex, 16)
            if hash_int < self._target:
                break
            else:
                nonce += 1

        return nonce, hash_hex
