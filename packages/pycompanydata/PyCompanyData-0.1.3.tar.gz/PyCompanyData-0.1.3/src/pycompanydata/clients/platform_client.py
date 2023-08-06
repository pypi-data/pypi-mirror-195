from typing import List

from pycompanydata.clients.base_client import BaseClient
from pycompanydata.data_types.pagination import PaginatedResponse
from pycompanydata.data_types.platform.company import Company
from pycompanydata.data_types.platform.connections import DataConnection
from pycompanydata.data_types.platform.datasetmetadata import DataSetMetadata
from pycompanydata.data_types.platform.datastatus import DataStatus
from pycompanydata.data_types.platform.syncsettings import SyncSettings
from pycompanydata.handlers.platform.companyhandler import CompanyHandler
from pycompanydata.handlers.platform.connectionhandler import ConnectionHandler
from pycompanydata.handlers.platform.datasetmetadatahandler import DataSetHandler
from pycompanydata.handlers.platform.datastatushandler import DataStatusHandler
from pycompanydata.handlers.platform.syncsettingshandler import SyncSettingHandler


class PlatformClient(BaseClient):
    def get_companies(self, query: str = None, order_by: str = None) -> List[Company]:
        """Gets all companies

        :return: A list of companies
        :rtype: List[Company]
        """
        company_handler = CompanyHandler(self.key, self.env)
        return company_handler.get_all_companies(query, order_by)

    def get_companies_page(
        self,
        page_number: int = 1,
        page_size: int = 100,
        query: str = None,
        order_by: str = None,
    ) -> PaginatedResponse[Company]:
        """Get a page of companies

        :return: A page of companies
        :rtype: PaginatedResponse[Company]
        """
        company_handler = CompanyHandler(self.key, self.env)
        return company_handler.get_pageof_companies(
            page_number, page_size, query, order_by
        )

    def get_company(self, company_id: str) -> Company:
        """Gets a single company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :return: A single company
        :rtype: Company
        """

        company_handler = CompanyHandler(self.key, self.env)
        company = company_handler.get_single_company(company_id)
        return company

    def get_sync_settings(self, company_id: str) -> SyncSettings:
        """Gets the sync settings for a single company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :return: Sync settings for a company
        :rtype: SyncSettings
        """

        sync_settings_handler = SyncSettingHandler(self.key, self.env)
        sync_settings = sync_settings_handler.get_sync_settings(company_id)
        return sync_settings

    def get_connections(self, company_id: str, **kwargs) -> List[DataConnection]:
        """Gets the connections for a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :return: List of all of a companies connections
        :rtype: DataConnectionPaginatedResponse
        """

        connection_handler = ConnectionHandler(self.key, self.env)
        connection = connection_handler.get_company_connections(company_id, **kwargs)
        return connection

    def get_connections_page(
        self, company_id: str, **kwargs
    ) -> PaginatedResponse[DataConnection]:
        """Gets the connections for a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :return: List of all of a companies connections
        :rtype: DataConnectionPaginatedResponse
        """

        connection_handler = ConnectionHandler(self.key, self.env)
        connection = connection_handler.get_pageof_company_connections(
            company_id, **kwargs
        )
        return connection

    def get_connection(self, company_id: str, connection_id: str) -> DataConnection:
        """Gets a single connection for a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :param connection_id: Unique identifier for a connection
        :type connection_id: str
        :return: The details of a single connection
        :rtype: DataConnection
        """

        connection_handler = ConnectionHandler(self.key, self.env)
        connection = connection_handler.get_single_company_connection(
            company_id, connection_id
        )
        return connection

    def get_data_sets(self, company_id: str, **kwargs) -> List[DataSetMetadata]:
        """Gets the metadata history for a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :return: A list of all the data sets and their metadata
        :rtype: List[DataSetMetadata]
        """

        data_set_metadata_handler = DataSetHandler(self.key, self.env)
        data_set_metadata_history = data_set_metadata_handler.get_all_data_sets(
            company_id, **kwargs
        )
        return data_set_metadata_history

    def get_data_sets_page(
        self,
        company_id: str,
        page_number: int = 1,
        page_size: int = 100,
        query: str = None,
        order_by: str = None,
    ) -> PaginatedResponse[DataSetMetadata]:
        """Gets the metadata history for a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :return: A list of all the data sets and their metadata
        :rtype: PaginatedResponse[DataSetMetadata]
        """

        data_set_metadata_handler = DataSetHandler(self.key, self.env)
        data_set_metadata_history = data_set_metadata_handler.get_page_of_data_sets(
            company_id, page_number, page_size, query, order_by
        )
        return data_set_metadata_history

    def get_data_set(self, company_id: str, data_set_id: str) -> DataSetMetadata:
        """Gets a single dataset for a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :param data_set_id: Unique identifier for a dataset
        :type data_set_id: str
        :return: The metadata for a single dataset
        :rtype: DataSetMetadata
        """
        data_set_metadata_handler = DataSetHandler(self.key, self.env)
        data_set_metadata = data_set_metadata_handler.get_single_data_set(
            company_id, data_set_id
        )
        return data_set_metadata

    def get_data_status(self, company_id: str) -> DataStatus:
        """Gets the current status of each dataset that a company has

        :param company_id: Unique identifier for a company
        :type company_id: str
        :return: Description of the current status of each dataset that the company has
        :rtype: DataStatus
        """
        data_status_handler = DataStatusHandler(self.key, self.env)
        data_status = data_status_handler.get_company_data_status(company_id)
        return data_status
