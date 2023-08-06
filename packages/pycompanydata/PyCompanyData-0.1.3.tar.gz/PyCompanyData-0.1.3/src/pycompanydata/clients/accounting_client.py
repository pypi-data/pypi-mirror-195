from typing import List

from pycompanydata.clients.platform_client import BaseClient
from pycompanydata.data_types.accounting.account_transactions import AccountTransaction
from pycompanydata.data_types.accounting.accounts import Account
from pycompanydata.data_types.accounting.bills import Bill
from pycompanydata.data_types.accounting.invoices import Invoice
from pycompanydata.data_types.accounting.payments import Payment
from pycompanydata.data_types.accounting.suppliers import Supplier
from pycompanydata.data_types.pagination import PaginatedResponse
from pycompanydata.handlers.accounting.account_transaction_handler import (
    AccountTransactionHandler,
)
from pycompanydata.handlers.accounting.accounts_handler import AccountsHandler
from pycompanydata.handlers.accounting.bills_handler import BillsHandler
from pycompanydata.handlers.accounting.invoices_handler import InvoicesHandler
from pycompanydata.handlers.accounting.payments_handler import PaymentsHandler
from pycompanydata.handlers.accounting.suppliers_handler import SuppliersHandler


class AccountingClient(BaseClient):
    def get_accounts(
        self, company_id: str, query: str = None, order_by: str = None
    ) -> List[Account]:
        """Gets all accounts from a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :param query: Query to filter data
        :type query: str
        :param order_by: Field to order results by
        :type: order_by: str
        :return: A list of accounts
        :rtype: List[Account]
        """

        accounts_handler = AccountsHandler(self.key, self.env)
        return accounts_handler.get_all_accounts(company_id, query, order_by)

    def get_accounts_page(
        self,
        company_id: str,
        page_number: int = 1,
        page_size: int = 1,
        query: str = None,
        order_by: str = None,
    ) -> PaginatedResponse[Account]:
        """Gets a page of accounts from a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :param page_number: Page number to query
        :type page_number: str
        :param page_size: Maximum number of results to return
        :type: page_size: str
        :param query: Query to filter data
        :type query: str
        :param order_by: Field to order results by
        :type: order_by: str
        :return: A list of account transactions
        :rtype: AccountTransactionsPaginatedResponse
        """

        accounts_handler = AccountsHandler(self.key, self.env)
        accounts = accounts_handler.get_pageof_accounts(
            company_id, page_number, page_size, query, order_by
        )
        return accounts

    def get_account(self, company_id: str, account_id: str) -> Account:
        """Gets a single account from a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :param account_id: Unique identifier for an account
        :type account_id: str
        :return: A single account object
        :rtype: Account
        """

        acccounts_handler = AccountsHandler(self.key, self.env)
        return acccounts_handler.get_single_account(company_id, account_id)

    def get_account_transactions(
        self,
        company_id: str,
        connection_id: str,
        query: str = None,
        order_by: str = None,
    ) -> List[AccountTransaction]:
        """Gets all account transactions from a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :param connection_id: Unique identifier for a company's connection
        :type connection_id: str
        :param query: Query to filter data
        :type query: str
        :param order_by: Field to order results by
        :type: order_by: str
        :return: A list of account transactions
        :rtype: AccountTransactionsPaginatedResponse
        """

        account_transaction_handler = AccountTransactionHandler(self.key, self.env)
        account_transactions = account_transaction_handler.get_all_account_transactions(
            company_id, connection_id, query, order_by
        )
        return account_transactions

    def get_account_transactions_page(
        self,
        company_id: str,
        connection_id: str,
        page_number: int = 1,
        page_size: int = 1,
        query: str = None,
        order_by: str = None,
    ) -> PaginatedResponse[AccountTransaction]:
        """Gets a page of account transactions from a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :param connection_id: Unique identifier for a company's connection
        :type connection_id: str
        :param page_number: Page number to query
        :type page_number: str
        :param page_size: Maximum number of results to return
        :type: page_size: str
        :param query: Query to filter data
        :type query: str
        :param order_by: Field to order results by
        :type: order_by: str
        :return: A list of account transactions
        :rtype: AccountTransactionsPaginatedResponse
        """

        account_transaction_handler = AccountTransactionHandler(self.key, self.env)
        account_transactions = (
            account_transaction_handler.get_pageof_account_transactions(
                company_id, connection_id, page_number, page_size, query, order_by
            )
        )
        return account_transactions

    def get_account_transaction(
        self, company_id: str, connection_id: str, account_transaction_id: str
    ) -> AccountTransaction:
        """Gets a single account transaction from a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :param connection_id: Unique identifier for a company's connection
        :type connection_id: str
        :param account_transaction_id: Unique identifier for an account transaction
        :type account_transaction_id: str
        :return: A single account transaction object
        :rtype: AccountTransaction
        """

        account_transaction_handler = AccountTransactionHandler(self.key, self.env)
        account_transaction = (
            account_transaction_handler.get_single_account_transaction(
                company_id, connection_id, account_transaction_id
            )
        )
        return account_transaction

    def get_bills(
        self, company_id: str, query: str = None, order_by: str = None
    ) -> List[Bill]:
        """Gets all bills from a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :param query: Query to filter data
        :type query: str
        :param order_by: Field to order results by
        :type: order_by: str
        :return: A list of bills
        :rtype: List[Bill]
        """

        bills_handler = BillsHandler(self.key, self.env)
        return bills_handler.get_all_bills(company_id, query, order_by)

    def get_bills_page(
        self,
        company_id: str,
        page_number: int = 1,
        page_size: int = 1,
        query: str = None,
        order_by: str = None,
    ) -> PaginatedResponse[Bill]:
        """Gets a page of bills from a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :param page_number: Page number to query
        :type page_number: str
        :param page_size: Maximum number of results to return
        :type: page_size: str
        :param query: Query to filter data
        :type query: str
        :param order_by: Field to order results by
        :type: order_by: str
        :return: A list of bill transactions
        :rtype: PaginatedResponse[Bill]
        """

        bills_handler = BillsHandler(self.key, self.env)
        bills = bills_handler.get_pageof_bills(
            company_id, page_number, page_size, query, order_by
        )
        return bills

    def get_bill(self, company_id: str, bill_id: str) -> Bill:
        """Gets a single bill from a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :param bill_id: Unique identifier for an bill
        :type bill_id: str
        :return: A single bill transaction object
        :rtype: Bill
        """

        bills_handler = BillsHandler(self.key, self.env)
        return bills_handler.get_single_bill(company_id, bill_id)

    def get_suppliers(
        self, company_id: str, query: str = None, order_by: str = None
    ) -> List[Supplier]:
        """Gets all suppliers from a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :param query: Query to filter data
        :type query: str
        :param order_by: Field to order results by
        :type: order_by: str
        :return: A list of suppliers
        :rtype: List[Supplier]
        """

        suppliers_handler = SuppliersHandler(self.key, self.env)
        return suppliers_handler.get_all_suppliers(company_id, query, order_by)

    def get_suppliers_page(
        self,
        company_id: str,
        page_number: int = 1,
        page_size: int = 1,
        query: str = None,
        order_by: str = None,
    ) -> PaginatedResponse[Supplier]:
        """Gets a page of suppliers from a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :param page_number: Page number to query
        :type page_number: str
        :param page_size: Maximum number of results to return
        :type: page_size: str
        :param query: Query to filter data
        :type query: str
        :param order_by: Field to order results by
        :type: order_by: str
        :return: A list of supplier transactions
        :rtype: PaginatedResponse[Supplier]
        """

        suppliers_handler = SuppliersHandler(self.key, self.env)
        suppliers = suppliers_handler.get_pageof_suppliers(
            company_id, page_number, page_size, query, order_by
        )
        return suppliers

    def get_supplier(self, company_id: str, supplier_id: str) -> Supplier:
        """Gets a single supplier from a company

        :param company_id: Unique identifier for a company
        :type company_id: str
        :param supplier_id: Unique identifier for an supplier
        :type supplier_id: str
        :return: A single supplier object
        :rtype: Supplier
        """
        suppliers_handler = SuppliersHandler(self.key, self.env)
        return suppliers_handler.get_single_supplier(company_id, supplier_id)

    def get_invoices(
        self, company_id: str, query: str = None, order_by: str = None
    ) -> List[Invoice]:
        """Gets all invoices for a company

        :param company_id: Unique identifier for a company
        :type company_id: str

        :param query: Query to pass to Codat API to filter results
        :type query: str

        :param order_by: Name of the field to order the results by.
            Defaults to ascending; prefix with `-` to sort in descending order.
        :type orderby: str

        :return: A list of invoices
        :rtype: List[Invoice]
        """
        invoice_handler = InvoicesHandler(self.key, self.env)
        return invoice_handler.get_all_invoices(company_id, query, order_by)

    def get_invoices_page(
        self,
        company_id: str,
        page_number: int = 1,
        page_size: int = 100,
        query: str = None,
        order_by: str = None,
    ) -> PaginatedResponse[Invoice]:
        """Gets a page of invoices for a company

        :param company_id: Unique identifier for a company
        :type company_id: str

        :param query: Query to pass to Codat API to filter results
        :type query: str

        :param order_by: Name of the field to order the results by.
            Defaults to ascending; prefix with `-` to sort in descending order.
        :type orderby: str

        :param page_number: Page number to retrieve.  Default: 1
        :type page_number: int

        :param page_size: Number of records to retrieve.  Default: 100
        :type page_size: int

        :return: A page of invoices
        :rtype: PaginatedResponse[Invoice]
        """
        invoice_handler = InvoicesHandler(self.key, self.env)
        return invoice_handler.get_pageof_invoices(
            company_id, page_number, page_size, query, order_by
        )

    def get_invoice(self, company_id: str, invoice_id: str) -> Invoice:
        """Gets an invoice (by ID) for a company

        :param company_id: Unique identifier for a company
        :type company_id: str

        :param invoice_id: Unique identifier for the invoice
        :type invoice_id: str

        :return: An invoice
        :rtype: Invoice
        """
        invoice_handler = InvoicesHandler(self.key, self.env)
        return invoice_handler.get_single_invoice(company_id, invoice_id)

    def get_payments(
        self, company_id: str, query: str = None, order_by: str = None
    ) -> List[Payment]:
        """ """
        payments_handler = PaymentsHandler(self.key, self.env)
        return payments_handler.get_all_payments(company_id, query, order_by)

    def get_payment_page(
        self,
        company_id: str,
        page_number: int = 1,
        page_size: int = 100,
        query: str = None,
        order_by: str = None,
    ) -> PaginatedResponse[Payment]:
        """ """
        payments_handler = PaymentsHandler(self.key, self.env)
        return payments_handler.get_page_of_payments(
            company_id, page_number, page_size, query, order_by
        )

    def get_payment(self, company_id: str, payment_id: str) -> Payment:
        """ """
        payments_handler = PaymentsHandler(self.key, self.env)
        return payments_handler.get_single_payment(company_id, payment_id)
