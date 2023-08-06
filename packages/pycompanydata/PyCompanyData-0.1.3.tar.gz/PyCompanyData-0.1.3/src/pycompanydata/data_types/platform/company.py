import datetime
from typing import List, Optional

from pydantic import BaseModel

from pycompanydata.data_types.accounting.account_transactions import AccountTransaction
from pycompanydata.data_types.accounting.accounts import Account
from pycompanydata.data_types.accounting.invoices import Invoice
from pycompanydata.data_types.platform.connections import DataConnection
from pycompanydata.data_types.platform.datasetmetadata import DataSetMetadata
from pycompanydata.handlers.accounting.account_transaction_handler import (
    AccountTransactionHandler,
)
from pycompanydata.handlers.accounting.accounts_handler import AccountsHandler
from pycompanydata.handlers.accounting.invoices_handler import InvoicesHandler
from pycompanydata.handlers.platform.connectionhandler import ConnectionHandler
from pycompanydata.handlers.platform.datasetmetadatahandler import DataSetHandler

from ...handlers.platform.datastatushandler import DataStatusHandler
from ...handlers.platform.syncsettingshandler import SyncSettingHandler
from .datastatus import DataStatus
from .syncsettings import SyncSettings


class Company(BaseModel):
    id: str
    name: str
    platform: str
    redirect: str
    created: Optional[datetime.datetime] = None
    lastSync: Optional[str] = None
    dataConnections: Optional[List[DataConnection]] = None
    createdByUserName: Optional[str] = None
    key: str = ""
    env: str = ""

    def _set_env_and_key(self, key: str, env: str):
        self.key: str = key
        self.env: str = env

    # TODO -> Reimplement

    # def get_connections(self) -> DataConnectionPaginatedResponse:

    #     connection_handler = ConnectionHandler(key=self.key, env=self.env)

    #     connection = connection_handler.get_company_connections(self.id)
    #     return connection

    def get_connection(self, connection_id: str) -> DataConnection:
        connection_handler = ConnectionHandler(key=self.key, env=self.env)

        connection = connection_handler.get_single_company_connection(
            self.id, connection_id
        )
        return connection

    def get_sync_settings(self) -> SyncSettings:

        sync_settings_handler = SyncSettingHandler(key=self.key, env=self.env)
        sync_settings = sync_settings_handler.get_sync_settings(self.id)
        return sync_settings

    def get_data_sets(self) -> List[DataSetMetadata]:

        data_set_metadata_handler = DataSetHandler(self.key, self.env)
        data_set_metadata_history = data_set_metadata_handler.get_all_data_sets(self.id)
        return data_set_metadata_history

    def get_data_set(self, data_set_id: str) -> DataSetMetadata:
        data_set_metadata_handler = DataSetHandler(self.key, self.env)
        data_set_metadata = data_set_metadata_handler.get_single_data_set(
            self.id, data_set_id
        )
        return data_set_metadata

    def get_data_status(self) -> DataStatus:
        data_status_handler = DataStatusHandler(self.key, self.env)
        data_status = data_status_handler.get_company_data_status(self.id)
        return data_status

    def get_accounts(self, **kwargs) -> List[Account]:

        connection_handler = AccountsHandler(self.key, self.env)
        connection = connection_handler.get_all_accounts(self.id, **kwargs)
        return connection

    def get_account(self, account_id: str) -> Account:

        accounts_handler = AccountsHandler(self.key, self.env)
        account = accounts_handler.get_single_account(self.id, account_id)
        return account

    def get_account_transactions(self, connection_id: str) -> List[AccountTransaction]:

        account_transaction_handler = AccountTransactionHandler(self.key, self.env)
        account_transactions = account_transaction_handler.get_all_account_transactions(
            self.id, connection_id
        )
        return account_transactions

    def get_account_transaction(
        self, connection_id: str, account_transaction_id: str
    ) -> AccountTransaction:

        account_transaction_handler = AccountTransactionHandler(self.key, self.env)
        account_transaction = (
            account_transaction_handler.get_single_account_transaction(
                self.id, connection_id, account_transaction_id
            )
        )
        return account_transaction

    def get_invoices(self, query: str = None, order_by: str = None) -> List[Invoice]:
        invoice_handler = InvoicesHandler(self.key, self.env)
        return invoice_handler.get_all_invoices(self.id, query, order_by)
