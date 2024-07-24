import pickle

import constants as const


def load_mixnodes():
    with open(f'{const.DATA_PATH}mixnodes.bin', 'rb') as f:
        mixnodes = pickle.load(f)
    return mixnodes


def load_gateways():
    with open(f'{const.DATA_PATH}gateways.bin', 'rb') as f:
        gateways = pickle.load(f)
    return gateways


def update_mixnodes(mixnodes):
    with open(f'{const.DATA_PATH}mixnodes.bin', 'wb') as f:
        pickle.dump(mixnodes, f)


def update_gateways(gateways):
    with open(f'{const.DATA_PATH}gateways.bin', 'wb') as f:
        pickle.dump(gateways, f)
