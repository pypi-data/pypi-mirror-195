from typing import List

from pycompanydata.data_types.pagination import PaginatedResponse
from pycompanydata.data_types.platform.company import Company
from pycompanydata.handlers.base import BaseHandler


def set_env_and_keys_for_many_companies(
    companies: List[Company], key: str, env: str
) -> None:
    for comp in companies:
        comp._set_env_and_key(key=key, env=env)


class CompanyHandler(BaseHandler):
    def get_all_companies(
        self, query: str = None, order_by: str = None
    ) -> List[Company]:
        companies: List[Company] = self._get_all_pages(
            Company, self.path, query=query, orderBy=order_by
        )
        # hack to pass the key and env so the companies so they can
        # instatiate handlers make rest calls
        set_env_and_keys_for_many_companies(companies, self.key, self.env)
        return companies

    def get_pageof_companies(
        self, page_number: int, page_size: int, query: str = None, order_by: str = None
    ) -> PaginatedResponse[Company]:
        companies: PaginatedResponse[Company] = self._get_paginated_response(
            Company,
            self.path,
            page=page_number,
            pageSize=page_size,
            query=query,
            orderBy=order_by,
        )
        # hack to pass the key and env so the companies so they can
        # instatiate handlers make rest calls
        set_env_and_keys_for_many_companies(companies.results, self.key, self.env)
        return companies

    def get_single_company(self, company_id: str) -> Company:
        result = self.client.get(self.path + company_id)
        company = Company(**result)
        # hack to pass the key and env so the datclass returned can
        # instatiate handlers make rest calls
        company._set_env_and_key(key=self.key, env=self.env)
        return company
