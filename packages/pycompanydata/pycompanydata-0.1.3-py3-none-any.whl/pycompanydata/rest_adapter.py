import os
import typing
from collections import namedtuple
from urllib.parse import urlencode

import requests
import requests.packages

from .data_types.platform.exceptions import CodatException

Environments = namedtuple("Environments", ["prod", "uat", "dev"])


class RestAdapter:
    def __init__(self, host: str, key: str) -> None:

        self.environments = Environments(
            "api.codat.io",
            "api-uat.codat.io",
            os.getenv("CODAT_DEV_ENV", "api.codat.io"),
        )
        try:
            if host == "prod":
                self.host = f"https://{self.environments.prod}/"
            elif host == "uat":
                self.host = f"https://{self.environments.uat}/"
            elif host == "dev":
                self.host = f"https://{self.environments.dev}/"
            else:
                raise TypeError("only prod or uat host allowed")
        except TypeError:
            raise

        self.headers = {"Authorization": f"Basic {key}"}

    def get(self, path: str, **kwargs) -> typing.Dict:
        if kwargs:
            query_params = urlencode(kwargs)
        else:
            query_params = ""
        url = self.host + path + "?" + query_params
        headers = self.headers
        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            raise CodatException(err)

        json_response = response.json()
        return json_response
