from transaction import CoinbaseTx
import utils
from db import Bucket
from collections import defaultdict


class UTXOSet():
    db_file = "utxo.db"
    utxo_bucket = "utxo"

    def __init__(self, blockchain):
        self._bucket = Bucket(UTXOSet.db_file, UTXOSet.utxo_bucket)
        self._bc = blockchain

    def reindex(self):
        self._bucket.reset()
        utxos = self._bc.find_utxo()

        for txid, outs in utxos.items():
            self._bucket.put(txid, utils.serialize(outs))
        self._bucket.save()

    def find_spendable_outputs(self, pubkey_hash, amount):
        account_amount = 0
        unspent_outputs = defaultdict(list)

        for tx_id, outs in self._bucket.kv.items():
            outs = utils.deserialize(outs)

            for out_idx, out in enumerate(outs):
                if out.is_locked_with_key(pubkey_hash) and account_amount < amount:
                    account_amount += out.value
                    unspent_outputs[tx_id].append(out_idx)

        return account_amount, unspent_outputs

    def update(self, block):
        for tx in block.transactions:
            if not isinstance(tx, CoinbaseTx):
                for vin in tx.vin:
                    update_outs = []
                    outs_bytes = self._bucket.get(vin.txid)
                    outs = utils.deserialize(outs_bytes)

                    for out_idx, out in enumerate(outs):
                        if out_idx != vin.vout:
                            update_outs.append(out)

                    if len(update_outs) == 0:
                        self._bucket.delete(vin.txid)
                    else:
                        self._bucket.put(
                            vin.txid, utils.serialize(update_outs))

            # Add new outputs
            new_outputs = [out for out in tx.vout]
            self._bucket.put(tx.id, utils.serialize(new_outputs))

        self._bucket.save()

    def print_utxo(self):
        utxos = []

        for _, outs in self._bucket.kv.items():
            outs = utils.deserialize(outs)
            for out in outs:
                print(out.value)

    def find_utxo(self, pubkey_hash):
        utxos = []

        for _, outs in self._bucket.kv.items():
            outs = utils.deserialize(outs)

            for out in outs:
                if out.is_locked_with_key(pubkey_hash):
                    utxos.append(out)

        return utxos

    @property
    def blockchain(self):
        return self._bc
