import click
from blockChain import BlockChain
from pow import PoW
from wallet import Wallet
from wallets import Wallets
from utxo_set import UTXOSet
from transaction import UTXOTx, CoinbaseTx
import utils


@click.group()
@click.pass_context
def cli(ctx):
    pass
    # print(ctx.obj['bc'])


@cli.command()
@click.option("--transaction", "-t", required=True, type=str)
@click.pass_context
def addblock(ctx, transaction):
    bc = ctx.obj['bc']
    bc.add_block(transaction)


@cli.command()
@click.pass_context
def printchain(ctx):
    bc = ctx.obj['bc']
    for block in bc.blocks():
        print(f"Height: {block.height}")
        print("Prev. hash: {0}".format(block.prev_block_hash))
        print("Data: {0}".format(block.transactions))
        print("Hash: {0}".format(block.hash))
        pow = PoW(block)
        print("PoW: {0}\n".format(pow.validate()))


@cli.command()
@click.option("--height", "-h", required=True, type=int)
@click.pass_context
def printblock(ctx, height):
    bc = ctx.obj['bc']
    try:
        for block in bc.blocks(height):
            print(f"Height: {block.height}")
            print("Prev. hash: {0}".format(block.prev_block_hash))
            print("Data: {0}".format(block.transactions))
            print("Hash: {0}".format(block.hash))
            pow = PoW(block)
            print("PoW: {0}\n".format(pow.validate()))
    except Exception as e:
        print(f"Cannot found block height: {e}")


@cli.command()
def createwallet():
    wallets = Wallets()
    wallet = Wallet()
    address = wallet.address
    wallets.add_wallet(address, wallet)
    wallets.save()

    print("Your new address: {}".format(address))


@cli.command()
@click.option("--address", "-a", required=True, type=str)
def createblockchain(address):
    bc = BlockChain(address)
    utxo_set = UTXOSet(bc)
    utxo_set.reindex()

    print('Done!')


@cli.command()
@click.option("--from_addr", "-from", required=True, type=str)
@click.option("--to_addr", "-to", required=True, type=str)
@click.option("--amount", required=True, type=int)
def send(from_addr, to_addr, amount):
    bc = BlockChain()
    utxo_set = UTXOSet(bc)

    tx = UTXOTx(from_addr, to_addr, amount, utxo_set)
    cb_tx = CoinbaseTx(from_addr)
    new_block = bc.MineBlock([cb_tx, tx])
    utxo_set.update(new_block)
    print('Success!')


@cli.command()
@click.option("--address", "-a", required=True, type=str)
def getbalance(address):
    bc = BlockChain()
    utxo_set = UTXOSet(bc)

    utxo_set.print_utxo()

    pubkey_hash = utils.address_to_pubkey_hash(address)
    utxos = utxo_set.find_utxo(pubkey_hash)
    balance = 0

    for out in utxos:
        balance += out.value

    print('Balance of {0}: {1}'.format(address, balance))


if __name__ == "__main__":
    bc = BlockChain()
    cli(obj={'bc': bc})
    # test()
