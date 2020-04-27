import pickle
import hashlib
import ecdsa
import binascii
import base58


def load_pkl(file_name):
    with open(file_name, 'rb') as f:
        obj = pickle.load(f)
    return obj


def encode(string, code="utf-8"):
    return string.encode(code)


def decode(string, code="utf-8"):
    return string.decode(code)


def sum256_hex(*args):
    m = hashlib.sha256()
    for arg in args:
        m.update(arg)
    return m.hexdigest()


def sum256_byte(*args):
    m = hashlib.sha256()
    for arg in args:
        m.update(arg)
    return m.digest()


def privatekey_to_publickey(key):
    sk = ecdsa.SigningKey.from_string(key, ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return '04' + decode(binascii.hexlify(vk.to_string()))


def hash_public_key(pubkey):
    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(hashlib.sha256(binascii.unhexlify(pubkey)).digest())
    return ripemd160.hexdigest()


def get_address(pubkey_hash):
    return base58.base58CheckEncode(0x00, pubkey_hash)


def address_to_pubkey_hash(address):
    return base58.base58CheckDecode(address)


def pubkey_to_verifykey(pub_key, curve=ecdsa.SECP256k1):
    vk_string = binascii.unhexlify(encode(pub_key[2:]))
    return ecdsa.VerifyingKey.from_string(vk_string, curve=curve)


def serialize(data):
    return pickle.dumps(data)


def deserialize(data):
    return pickle.loads(data)
