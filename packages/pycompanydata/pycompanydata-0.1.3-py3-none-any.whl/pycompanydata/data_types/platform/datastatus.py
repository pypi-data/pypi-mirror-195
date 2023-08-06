import datetime
from typing import Optional

from pydantic import BaseModel


class DataTypeStatus(BaseModel):
    dataType: str
    lastSuccessfulSync: Optional[datetime.datetime] = None
    currentStatus: Optional[str] = None
    latestSyncId: Optional[str] = None
    latestSuccessfulSyncId: Optional[str] = None


class DataStatus(BaseModel):
    chartOfAccounts: Optional[DataTypeStatus] = None
    bills: Optional[DataTypeStatus] = None
    billPayments: Optional[DataTypeStatus] = None
    company: Optional[DataTypeStatus] = None
    creditNotes: Optional[DataTypeStatus] = None
    customers: Optional[DataTypeStatus] = None
    invoices: Optional[DataTypeStatus] = None
    journals: Optional[DataTypeStatus] = None
    journalEntries: Optional[DataTypeStatus] = None
    payments: Optional[DataTypeStatus] = None
    suppliers: Optional[DataTypeStatus] = None
    balanceSheet: Optional[DataTypeStatus] = None
    profitAndLoss: Optional[DataTypeStatus] = None
    taxRates: Optional[DataTypeStatus] = None
    items: Optional[DataTypeStatus] = None
    bankAccounts: Optional[DataTypeStatus] = None
    bankTransactions: Optional[DataTypeStatus] = None
    billCreditNotes: Optional[DataTypeStatus] = None
    trackingCategories: Optional[DataTypeStatus] = None
    cashFlowStatement: Optional[DataTypeStatus] = None
    purchaseOrders: Optional[DataTypeStatus] = None
    accountTransactions: Optional[DataTypeStatus] = None
    transfers: Optional[DataTypeStatus] = None
    directCosts: Optional[DataTypeStatus] = None
    directIncomes: Optional[DataTypeStatus] = None
    paymentMethods: Optional[DataTypeStatus] = None
    salesOrders: Optional[DataTypeStatus] = None
