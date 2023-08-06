from typing import List

from pycompanydata.data_types.pagination import PaginatedResponse
from pycompanydata.data_types.platform.connections import DataConnection
from pycompanydata.handlers.base import BaseHandler


class ConnectionHandler(BaseHandler):
    def get_company_connections(
        self, company_id: str, **kwargs
    ) -> List[DataConnection]:
        connections: List[DataConnection] = self._get_all_pages(
            DataConnection, self.path + company_id + "/connections", **kwargs
        )
        return connections

    def get_pageof_company_connections(
        self, company_id: str, **kwargs
    ) -> PaginatedResponse[DataConnection]:
        companies: PaginatedResponse[DataConnection] = self._get_paginated_response(
            DataConnection, self.path + company_id + "/connections", **kwargs
        )
        return companies

    def get_single_company_connection(
        self, company_id: str, connection_id: str
    ) -> DataConnection:
        result = self.client.get(
            self.path + company_id + "/connections/" + connection_id
        )
        return DataConnection(**result)
