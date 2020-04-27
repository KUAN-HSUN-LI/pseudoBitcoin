from block import Block
from db import DB, Bucket
from utils import decode
import pickle
from transaction import CoinbaseTx
from collections import defaultdict


class BlockChain():
    latest = 'l'
    latest_height = 'height'
    db_file = "blockchain.db"
    block_bucket = 'blocks'
    genesis_coinbase_data = 'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks'

    def __init__(self, address=None):
        self._bucket = Bucket(BlockChain.db_file, BlockChain.block_bucket)
        self._db = DB(BlockChain.db_file)

        try:
            self._tip = self._bucket.get('l')
        except KeyError:
            if not address:
                self._tip = None
            else:
                cb_tx = CoinbaseTx(address, BlockChain.genesis_coinbase_data)
                genesis = Block([cb_tx], 0).proof_of_block()
                self._put_block(genesis)

    def _put_block(self, block):
        self._bucket.put(block.hash, block.serialize())
        self._bucket.put('l', block.hash)
        self._bucket.put('height', block.height)
        self._tip = block.hash
        self._bucket.commit()

    def MineBlock(self, tx_lst):
        last_hash = self._bucket.get('l')
        last_height = self._bucket.get('height')

        for tx in tx_lst:
            if not self.verify_transaction(tx):
                print("ERROR: Invalid transaction")
                sys.exit()

        new_block = Block(tx_lst, last_height+1, last_hash).proof_of_block()
        self._put_block(new_block)
        return new_block

    def find_unspent_transactions(self, pubkey_hash):
        spent_txo = defaultdict(list)
        unspent_txs = []
        for block in blocks:
            for tx in block.transactions:

                if not isinstance(tx, CoinbaseTx):
                    for vin in tx.vin:
                        if vin.uses_key(pubkey_hash):
                            spent_txo[tx.id].append(vin.vout)
                for out_idx, out in enumerate(tx.vout):
                    if spent_txo[tx.id]:
                        for spent_out in spent_txo[tx.id]:
                            if spent_out == out_idx:
                                continue
                    if out.is_locked_with_key(pubkey_hash):
                        unspent_txs.append(tx)
                        break
        return unspent_txs

    def find_utxo(self):
        utxo = defaultdict(list)
        spent_txos = defaultdict(list)

        for block in self.blocks():
            for tx in block.transactions:

                for out_idx, out in enumerate(tx.vout):
                    if spent_txos[tx.id]:
                        for spent_out in spent_txos[tx.id]:
                            if spent_out == out_idx:
                                continue

                    utxo[tx.id].append(out)

                if not isinstance(tx, CoinbaseTx):
                    for vin in tx.vin:
                        spent_txos[vin.txid].append(vin.vout)

        return utxo

    def add_block(self, data):
        last_hash = decode(self._db.get(BlockChain.latest))
        new_height = int(self._db.get(BlockChain.latest_height)) + 1
        new_block = Block(data, new_height, prev_block_hash=last_hash).proof_of_block()

        self._db.put(new_block.hash, pickle.dumps(new_block))
        self._db.put(BlockChain.latest_height, new_block.height)
        self._db.put(BlockChain.latest, new_block.hash)
        self._tip = new_block.hash

    # @property
    def blocks(self, height=None):
        cur_tip = self._tip
        while True:
            if not cur_tip:
                break
            encoded_block = self._bucket.get(cur_tip)
            block = pickle.loads(encoded_block)
            cur_tip = block.prev_block_hash
            cur_height = block.height
            if height:
                if cur_height == height:
                    yield block
                    return
                elif cur_height < height:
                    raise IndexError(height)
                else:
                    pass
            yield block

    # ???
    def find_transaction(self, ID):
        for block in self.blocks():
            for tx in block.transactions:
                if tx.id == ID:
                    return tx

        return None

    # ???
    def sign_transaction(self, tx, priv_key):
        prev_txs = {}
        for vin in tx.vin:
            prev_tx = self.find_transaction(vin.txid)
            prev_txs[prev_tx.id] = prev_tx

        tx.sign(priv_key, prev_txs)

    # ???
    def verify_transaction(self, tx):
        if isinstance(tx, CoinbaseTx):
            return True

        prev_txs = {}
        for vin in tx.vin:
            prev_tx = self.find_transaction(vin.txid)
            prev_txs[prev_tx.id] = prev_tx

        return tx.verify(prev_txs)
