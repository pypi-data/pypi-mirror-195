from typing import Any, Dict

import requests

from knapsack.api import Api
from knapsack.knapsack_dataset import KnapsackDataset

def post(
    endpoint: str,
    info: Dict[str, Any] = None,
    **kwargs
) -> None:
    json = dict(kwargs)
    json['info'] = info
    result = requests.post(Api.BASE_URL + "/" + endpoint, json=json)
    return result
