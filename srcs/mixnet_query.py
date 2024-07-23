import requests
import sys

import constants as const


def get_node_score(id, node_type):
    if node_type == "mixnode":
        url = f'{const.MIXNODE_API}{id}/report'
    else:
        url = f'{const.GATEWAY_API}{id}/report'

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

    return json_response['last_day']
