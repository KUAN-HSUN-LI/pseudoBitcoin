import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--addBlock")
    parser.add_argument("--printChain")
    parser.add_argument("--printBlock")
    parser.add_argument("--createBlockChain")
    parser.add_argument("--getBalance")
    parser.add_argument("--send")
    parser.add_argument("--address")
    args = parser.parse_args()
    return args
