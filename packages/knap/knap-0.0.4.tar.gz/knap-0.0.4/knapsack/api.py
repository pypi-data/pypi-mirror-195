import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List

import aiohttp
import requests
from aiohttp import ClientSession


class RequestType(Enum):
    GET = "GET"
    POST = "POST"


class Api(object):
    BASE_URL: str = "https://knap.ai"

    DEFAULT_API_KEY_DIR: str = os.path.expanduser("~/.knapsack_local/api_keys")

    def __init__(self) -> None:
        self.org_names_to_api_keys = {}
        self.org_names_to_api_keys = self._init_api_keys()

    def _init_api_keys(self) -> Dict[str, str]:
        api_keys = self._get_api_keys()
        response = self.GET(
            endpoint="org_names", org_name="",
            info={"api_keys": api_keys}
        )
        org_names = response.json()['orgNames']
        org_names_to_api_keys = {}
        if org_names is None or len(org_names) <= 0:
            return {}
        for i, org_name in enumerate(org_names):
            org_names_to_api_keys[org_name] = api_keys[i]
        return org_names_to_api_keys

    def _get_api_keys(self) -> List[str]:
        api_key_dir = os.environ.get('KNAPSACK_API_KEY_DIR')
        if api_key_dir is not None:
            env_api_key_dir = Path(os.environ.get('KNAPSACK_API_KEY_DIR'))
            if env_api_key_dir.exists():
                return self._read_api_keys_from_dir(env_api_key_dir)
        elif Path(self.DEFAULT_API_KEY_DIR).exists():
            return self._read_api_keys_from_dir(self.DEFAULT_API_KEY_DIR)
        else:
            raise ValueError(
                "No API keys found in either env var KNAPSACK_API_KEY_DIR " +
                "or in ~/.knapsack_local/api_keys. Make sure that your API " +
                "key ends with \".key\"."
            )

    def _read_api_keys_from_dir(self, dir_path: Path) -> List[str]:
        key_filenames = os.listdir(str(dir_path))
        api_keys = []
        for key_filename in key_filenames:
            key_file = dir_path / Path(key_filename)
            if key_file.suffix == ".key":
                with open(key_file, 'r') as f:
                    api_key = f.readline()
                    api_key = api_key.strip()
                    api_keys.append(api_key)
        return api_keys

    def GET(
        self,
        endpoint: str,
        org_name: str,
        info: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        api_key = self.org_names_to_api_keys.get(org_name, "")
        if api_key != "":
            info["api_key"] = api_key
        result = requests.get(self.BASE_URL + "/" + endpoint, json=info)
        return result

    def POST(
        self,
        endpoint: str,
        org_name: str,
        info: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        info["api_key"] = self.org_names_to_api_keys.get(org_name, "")
        result = requests.post(self.BASE_URL + "/" + endpoint, json=info)
        return result

    async def async_request(
        self,
        session: ClientSession,
        method: RequestType,
        endpoint: str,
        info: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        info["api_key"] = self._load_api_key()
        try:
            result = await session(
                method=str(method),
                url=self.BASE_URL + "/" + endpoint,
                json=info
            )
        except (
            aiohttp.ClientError,
            aiohttp.http_exceptions.HttpProcessingError,
        ) as e:
            print(f"Error sending async request: {e}")
            return None
        print(f"{method} result: ", result)
        return result
