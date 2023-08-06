import typing

from pycompanydata.data_types.accounting.accounts import Account
from pycompanydata.data_types.pagination import PaginatedResponse
from pycompanydata.handlers.base import BaseHandler


class AccountsHandler(BaseHandler):
    def get_all_accounts(
        self, company_id: str, query: str = None, order_by: str = None
    ) -> typing.List[Account]:
        path = f"{self.path}{company_id}/data/accounts"
        return self._get_all_pages(Account, path, query=query, orderBy=order_by)

    def get_pageof_accounts(
        self,
        company_id: str,
        page_number: int,
        page_size: int,
        query: str = None,
        order_by: str = None,
    ) -> PaginatedResponse[Account]:
        path = f"{self.path}{company_id}/data/accounts"
        return self._get_paginated_response(
            Account,
            path,
            page=page_number,
            pageSize=page_size,
            query=query,
            orderBy=order_by,
        )

    def get_single_account(self, company_id: str, account_id: str) -> Account:
        path = f"{self.path}{company_id}/data/accounts/{account_id}"
        account = self.client.get(path)
        return Account(**account)
