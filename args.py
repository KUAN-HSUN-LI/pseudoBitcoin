import click
from blockChain import BlockChain
from pow import PoW
from wallet import Wallet
from wallets import Wallets
from utxo_set import UTXOSet
from transaction import UTXOTx, CoinbaseTx
import utils
import sys
from click_shell import shell


@shell(prompt='cmd > ', intro='Starting pseudo bitcoin...', context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("--name", "-n", required=True, help="Enter client's name")
@click.pass_context
def cli(ctx, name):
    ctx.obj['name'] = name


@cli.command()
@click.pass_context
def printchain(ctx):
    bc = BlockChain()
    for block in bc.blocks():
        print(f"Height: {block.height}")
        print(f"Prev. hash: {block.prev_block_hash}")
        print(f"Data: {block.transactions}")
        print(f"Hash: {block.hash}")
        pow = PoW(block)
        print(f"PoW: {pow.validate()}\n")


@cli.command()
@click.option("--height", "-h", required=True, type=int)
@click.pass_context
def printblock(ctx, height):
    bc = BlockChain()
    if height < 0:
        print(f"Block height must >= 0, but get height {height}")
        sys.exit()
    try:
        for block in bc.blocks(height):
            print(f"Height: {block.height}")
            print(f"Prev. hash: {block.prev_block_hash}")
            print(f"Data: {block.transactions}")
            print(f"Hash: {block.hash}")
            pow = PoW(block)
            print(f"PoW: {pow.validate()}\n")
    except Exception as e:
        print(f"Cannot found block height: {e}")


@cli.command()
def createwallet():
    wallets = Wallets()
    wallet = Wallet()
    address = wallet.address
    wallets.add_wallet(address, wallet)
    wallets.save()

    print(f"Your new address: {address}")


@cli.command()
def getwallets():
    wallets = Wallets()
    for idx, addr in enumerate(wallets.get_addresses()):
        print(f"address{idx}: {addr}")


@cli.command()
@click.option("--address", "-a", required=True, type=str)
@click.pass_context
def createblockchain(ctx, address):
    bc = BlockChain(address)
    utxo_set = UTXOSet(bc)
    utxo_set.reindex()

    print('Done!')


@cli.command()
@click.option("--from_addr", "-from", required=True, type=str)
@click.option("--to_addr", "-to", required=True, type=str)
@click.option("--amount", "-a", required=True, type=int)
@click.pass_context
def send(ctx, from_addr, to_addr, amount):
    bc = BlockChain()
    utxo_set = UTXOSet(bc)

    tx = UTXOTx(from_addr, to_addr, amount, utxo_set)
    cb_tx = CoinbaseTx(from_addr)
    new_block = bc.MineBlock([cb_tx, tx])
    utxo_set.update(new_block)
    print('Success!')


@cli.command()
@click.option("--address", "-a", required=True, type=str)
@click.pass_context
def getbalance(ctx, address):
    bc = BlockChain()
    utxo_set = UTXOSet(bc)

    # utxo_set.print_utxo()

    pubkey_hash = utils.address_to_pubkey_hash(address)
    utxos = utxo_set.find_utxo(pubkey_hash)
    balance = 0

    for out in utxos:
        balance += out.value

    print('Balance of {0}: {1}'.format(address, balance))


if __name__ == "__main__":
    cli(obj={})
