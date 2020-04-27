from blockChain import BlockChain
from pow import PoW

if __name__ == '__main__':
    bc = BlockChain()
    bc.add_block("Send 1 BTC to Ivan")
    bc.add_block("Send 2 more BTC to Ivan")
    for block in bc.blocks:
        print(f"Height: {block.height}")
        print("Prev. hash: {0}".format(block.prev_block_hash))
        print("Data: {0}".format(block.transactions))
        print("Hash: {0}".format(block.hash))
        pow = PoW(block)
        print("PoW: {0}\n".format(pow.validate()))
