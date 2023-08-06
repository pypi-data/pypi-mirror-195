from typing import List

from pycompanydata.data_types.accounting.account_transactions import AccountTransaction
from pycompanydata.data_types.pagination import PaginatedResponse
from pycompanydata.handlers.base import BaseHandler


class AccountTransactionHandler(BaseHandler):
    def get_all_account_transactions(
        self,
        company_id: str,
        connection_id: str,
        query: str = None,
        order_by: str = None,
    ) -> List[AccountTransaction]:
        path = f"{self.path}{company_id}/connections/{connection_id}/data/accounttransactions"
        return self._get_all_pages(
            AccountTransaction, path, query=query, orderBy=order_by
        )

    def get_pageof_account_transactions(
        self,
        company_id: str,
        connection_id: str,
        page_number: int,
        page_size: int,
        query: str = None,
        order_by: str = None,
    ) -> PaginatedResponse[AccountTransaction]:
        path = f"{self.path}{company_id}/connections/{connection_id}/data/accounttransactions"
        return self._get_paginated_response(
            AccountTransaction,
            path,
            page=page_number,
            pageSize=page_size,
            query=query,
            orderBy=order_by,
        )

    def get_single_account_transaction(
        self, company_id: str, connection_id: str, account_transaction_id: str
    ) -> AccountTransaction:
        path = f"""{self.path}{company_id}
            /connections/{connection_id}/data/accounttransactions/{account_transaction_id}"""
        account_transaction = self.client.get(path)
        return AccountTransaction(**account_transaction)
