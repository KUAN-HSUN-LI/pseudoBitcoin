import sys
import pickle
import copy
import wallets as ws
import utils
from transaction_output import TXOuput
from transaction_input import TXInput
import ecdsa


class Transaction():
    def __init__(self, txid=None, vin=None, vout=None):
        self._id = txid
        self._vin = vin
        self._vout = vout

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def vin(self):
        return self._vin

    @property
    def vout(self):
        return self._vout

    def set_id(self):
        self._id = self.hash()
        return self

    def hash(self):
        return utils.sum256_hex(pickle.dumps(self))

    def _trimmed_copy(self):
        inputs = []
        outputs = []

        for vin in self.vin:
            inputs.append(TXInput(vin.txid, vin.vout, None, None))

        for vout in self.vout:
            outputs.append(TXOuput(vout.value, vout.address))

        return Transaction(self.id, inputs, outputs)

    def sign(self, private_key, prev_txs):
        # for vin in self.vin:
        #     if not prev_txs[vin.tx_id].ID:
        #         # log.error("Previous transaction is not correct")
        #         print("Previous transaction is not correct")

        tx_copy = self._trimmed_copy()

        for in_id, vin in enumerate(tx_copy.vin):
            prev_tx = prev_txs[vin.txid]
            tx_copy.vin[in_id].public_key = prev_tx.vout[vin.vout].public_key_hash
            tx_copy.id = tx_copy.hash()
            tx_copy.vin[in_id].public_key = None

            sk = ecdsa.SigningKey.from_string(
                private_key, curve=ecdsa.SECP256k1)
            sig = sk.sign(utils.encode(tx_copy.id))

            self.vin[in_id].signature = sig

    def verify(self, prev_txs):
        # for vin in self.vin:
        #     if not prev_txs[vin.tx_id].ID:
        #         # log.error("Previous transaction is not correct")
        #         print("Previous transaction is not correct")
        tx_copy = self._trimmed_copy()

        for in_id, vin in enumerate(self.vin):
            prev_tx = prev_txs[vin.txid]
            tx_copy.vin[in_id].public_key = prev_tx.vout[vin.vout].public_key_hash
            tx_copy.id = tx_copy.hash()
            tx_copy.vin[in_id].public_key = None

            sig = self.vin[in_id].signature
            # vk = ecdsa.VerifyingKey.from_string(
            #     vin.public_key[2:], curve=ecdsa.SECP256k1)
            vk = utils.pubkey_to_verifykey(vin.public_key)
            if not vk.verify(sig, utils.encode(tx_copy.id)):
                return False

        return True


class CoinbaseTx(Transaction):
    def __init__(self, to, data=None):
        if not data:
            data = f"Reward to {to}"

        txid = None
        vin = [TXInput('', -1, None, data)]
        vout = [TXOuput(TXOuput.subsidy, to)]

        self._tx = Transaction(txid, vin, vout).set_id()

    @property
    def id(self):
        return self._tx.id

    @property
    def vin(self):
        return self._tx.vin

    @property
    def vout(self):
        return self._tx.vout

    def to_bytes(self):
        return utils.serialize(self)


class UTXOTx(Transaction):
    def __init__(self, from_addr, to_addr, amount, utxo_set):
        inputs = []
        outputs = []

        wallets = ws.Wallets()
        wallet = wallets.get_wallet(from_addr)
        pubkey_hash = utils.hash_public_key(wallet.public_key)

        acc, valid_outputs = utxo_set.find_spendable_outputs(pubkey_hash, amount)

        if acc < amount:
            print("Not enough funds")
            sys.exit()

        for tx_idx, outs in valid_outputs.items():
            for out in outs:
                inputs.append(TXInput(tx_idx, out, None, wallet.public_key))
        outputs.append(TXOuput(amount, to_addr))
        if acc > amount:
            outputs.append(TXOuput(acc-amount, from_addr))

        self._tx = Transaction(None, inputs, outputs).set_id()
        self._utxo_set = utxo_set
        self._sign_utxo(wallet.private_key)

    @property
    def id(self):
        return self._tx.id

    @property
    def vin(self):
        return self._tx.vin

    @property
    def vout(self):
        return self._tx.vout

    def _sign_utxo(self, private_key):
        self._utxo_set.blockchain.sign_transaction(self._tx, private_key)

    def sign(self, private_key, prev_tx):
        self._tx.sign(private_key, prev_tx)

    def verify(self, prev_tx):
        return self._tx.verify(prev_tx)

    def to_bytes(self):
        return utils.serialize(self)
