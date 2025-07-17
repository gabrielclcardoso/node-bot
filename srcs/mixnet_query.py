import requests
import sys

import constants as const


def get_node_score(id):
    url = f'{const.API}{id}'

    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError as e:
        print(e, file=sys.stderr)
        raise

    if response.status_code != 200:
        error = f'Bad respose on {url} -> {response.status_code}'
        print(error, file=sys.stderr)
        raise Exception(error)

    try:
        json_response = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(e, file=sys.stderr)
        raise

    return float(json_response['annotation']['last_24h_performance'])


def node_exists(id):
    url = f'{const.API}{id}'

    try:
        response = requests.get(url)
    except Exception:
        return False

    if response.status_code != 200:
        return False
    return True
