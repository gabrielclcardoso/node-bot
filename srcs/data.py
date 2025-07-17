import pickle

import constants as const

NODES = set()


def load_nodes():
    with open(f'{const.DATA_PATH}nodes.bin', 'rb') as f:
        nodes = pickle.load(f)
    return nodes


def update_nodes(nodes):
    with open(f'{const.DATA_PATH}nodes.bin', 'wb') as f:
        pickle.dump(nodes, f)
