import requests
import sys

import constants as const


def get_mixnode_score(id):
    url = f'{const.API}mix-node/{id}'

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

    return json_response['avg_uptime']
