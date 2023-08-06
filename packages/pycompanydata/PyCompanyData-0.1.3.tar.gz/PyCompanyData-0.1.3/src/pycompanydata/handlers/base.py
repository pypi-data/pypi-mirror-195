from typing import Any, List, TypeVar

from pycompanydata.data_types.pagination import PaginatedResponse
from pycompanydata.rest_adapter import RestAdapter

T = TypeVar("T")


class BaseHandler:
    def __init__(self, key: str, env: str) -> None:
        self.key = key
        self.env = env
        self.client = RestAdapter(host=env, key=key)
        self.path = "companies/"

    def _get_paginated_response(
        self, model: Any, path: str, **kwargs
    ) -> PaginatedResponse[T]:
        kwargs = {key: value for key, value in kwargs.items() if value is not None}
        response = self.client.get(path, **kwargs)
        return PaginatedResponse[model](**response)  # type: ignore  # this does give the desired behaviour,
        # the static type checker just doesnt like it
        #  https://stackoverflow.com/questions/59634937/variable-foo-class-is-not-valid-as-type-but-why

    def _get_all_pages(self, model, path, **kwargs) -> List[T]:
        page_number = 1
        results = []
        while True:
            response: PaginatedResponse = self._get_paginated_response(
                model, path, page=page_number, pageSize=100, **kwargs
            )
            results += response.results
            page_number += 1
            if not response.links.next:
                break
        return results
