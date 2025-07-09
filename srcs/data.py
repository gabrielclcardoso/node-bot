import pickle

import constants as const


def load_gateways():
    with open(f'{const.DATA_PATH}nodes.bin', 'rb') as f:
        gateways = pickle.load(f)
    return gateways


def update_nodes(nodes):
    with open(f'{const.DATA_PATH}gateways.bin', 'wb') as f:
        pickle.dump(nodes, f)
