from typing import List

from pycompanydata.data_types.accounting.suppliers import Supplier
from pycompanydata.data_types.pagination import PaginatedResponse
from pycompanydata.handlers.base import BaseHandler


class SuppliersHandler(BaseHandler):
    def get_all_suppliers(
        self, company_id: str, query: str = None, order_by: str = None
    ) -> List[Supplier]:
        path = f"{self.path}{company_id}/data/suppliers"
        return self._get_all_pages(Supplier, path, query=query, orderBy=order_by)

    def get_pageof_suppliers(
        self,
        company_id: str,
        page_number: int,
        page_size: int,
        query: str = None,
        order_by: str = None,
    ) -> PaginatedResponse[Supplier]:
        path = f"{self.path}{company_id}/data/suppliers"
        return self._get_paginated_response(
            Supplier,
            path,
            page=page_number,
            pageSize=page_size,
            query=query,
            orderBy=order_by,
        )

    def get_single_supplier(self, company_id: str, supplier_id: str) -> Supplier:
        path = f"{self.path}{company_id}/data/suppliers/{supplier_id}"
        account = self.client.get(path)
        return Supplier(**account)
