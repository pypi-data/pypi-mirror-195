from typing import List

from pycompanydata.data_types.pagination import PaginatedResponse
from pycompanydata.data_types.platform.datasetmetadata import DataSetMetadata
from pycompanydata.handlers.base import BaseHandler


class DataSetHandler(BaseHandler):

    path = "companies/"

    def get_all_data_sets(self, company_id: str, **kwargs) -> List[DataSetMetadata]:
        data_sets: List[DataSetMetadata] = self._get_all_pages(
            DataSetMetadata, self.path + company_id + "/data/history", **kwargs
        )
        return data_sets

    def get_page_of_data_sets(
        self,
        company_id: str,
        page_number: int,
        page_size: int,
        query: str = None,
        order_by: str = None,
    ) -> PaginatedResponse[DataSetMetadata]:
        data_sets: PaginatedResponse[DataSetMetadata] = self._get_paginated_response(
            DataSetMetadata,
            self.path + company_id + "/data/history",
            page=page_number,
            pageSize=page_size,
            query=query,
            orderBy=order_by,
        )
        return data_sets

    def get_single_data_set(self, company_id: str, data_set_id: str) -> DataSetMetadata:
        result = self.client.get(
            self.path + company_id + "/data/history/" + data_set_id
        )
        return DataSetMetadata(**result)
