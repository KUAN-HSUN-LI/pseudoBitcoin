class PoW():
    def __init__(self, block):
        self._block = block
        self._target = 1 << (256 – block.bits)

    def prepare_data(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError

    def validate(self):
        raise NotImplementedError
