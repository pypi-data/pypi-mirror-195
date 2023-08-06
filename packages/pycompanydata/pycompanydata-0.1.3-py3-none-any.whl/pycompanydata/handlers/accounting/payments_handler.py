import typing

from pycompanydata.data_types.accounting.payments import Payment
from pycompanydata.data_types.pagination import PaginatedResponse
from pycompanydata.handlers.base import BaseHandler


class PaymentsHandler(BaseHandler):
    def get_all_payments(
        self, company_id: str, query: str = None, order_by: str = None
    ) -> typing.List[Payment]:
        path = f"{self.path}{company_id}/data/payments"
        return self._get_all_pages(Payment, path, query=query, orderBy=order_by)

    def get_page_of_payments(
        self,
        company_id: str,
        page_number: int,
        page_size: int,
        query: str = None,
        order_by: str = None,
    ) -> PaginatedResponse[Payment]:
        path = f"{self.path}{company_id}/data/payments"
        return self._get_paginated_response(
            Payment,
            path,
            page=page_number,
            pageSize=page_size,
            query=query,
            orderBy=order_by,
        )

    def get_single_payment(self, company_id: str, payment_id: str) -> Payment:
        path = f"{self.path}{company_id}/data/payments/{payment_id}"
        payment = self.client.get(path)
        return Payment(**payment)
