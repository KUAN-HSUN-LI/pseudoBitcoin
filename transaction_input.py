import utils


class TXInput():
    def __init__(self, txid, vout, sig, pubkey):
        self._txid = utils.encode(txid)
        self._vout = vout
        self._sig = sig
        self._public_key = pubkey

    def uses_key(self, pubkey_hash):
        return pubkey_hash == utils.hash_public_key(self.pubkey)

    @property
    def txid(self):
        return utils.decode(self._txid)

    @property
    def vout(self):
        return self._vout

    @property
    def signature(self):
        return self._sig

    @property
    def public_key(self):
        return self._public_key

    @signature.setter
    def signature(self, sig):
        self._sig = sig

    @public_key.setter
    def public_key(self, public_key):
        self._public_key = public_key
