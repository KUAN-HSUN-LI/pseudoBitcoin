import utils


class TXOuput():
    subsidy = 10

    def __init__(self, value, address):
        self._value = value
        self._address = address
        self._public_key_hash = utils.address_to_pubkey_hash(address)

    def is_locked_with_key(self, pubkey_hash):
        return self._public_key_hash == pubkey_hash

    @property
    def value(self):
        return self._value

    @property
    def address(self):
        return self._address

    @property
    def public_key_hash(self):
        return self._public_key_hash
