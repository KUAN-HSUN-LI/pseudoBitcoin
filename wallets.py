import pickle
from utils import load_pkl
import sys


class Wallets():

    wallet_file = "wallet.pkl"

    def __init__(self):
        try:
            self.wallets = load_pkl(self.wallet_file)
        except FileNotFoundError:
            self.wallets = {}

    def add_wallet(self, addr, wallet):
        self.wallets[addr] = wallet

    def get_addresses(self):
        return [addr for addr in self.wallets.keys()]

    def get_wallet(self, addr):
        try:
            return self.wallets[addr]
        except KeyError:
            print(f"Cannot find wallet {addr}")
            sys.exit()

    def save(self):
        with open(self.wallet_file, 'wb') as f:
            pickle.dump(self.wallets, f)
