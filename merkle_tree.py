import utils


class MerkleNode():
    def __init__(self, left, right, data):
        self.left = left
        self.right = right
        if left is None and right is None:
            self.data = utils.sum256_byte(data)
        else:
            self.data = utils.sum256_byte(left.data, right.data)


class MerkleTree():
    def __init__(self, data_lst):
        nodes = []

        if len(data_lst) % 2 != 0:
            data_lst.append(data_lst[-1])

        for data in data_lst:
            nodes.append(MerkleNode(None, None, data))

        for i in range(len(data_lst) // 2):
            next_level = []
            for j in range(0, len(nodes), 2):
                next_level.append(MerkleNode(nodes[j], nodes[j+1], None))

            nodes = next_level

        self._root = nodes[0]

    @property
    def root(self):
        return self._root

    @property
    def root_hash(self):
        return self._root.data
