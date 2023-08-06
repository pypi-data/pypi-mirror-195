from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from pycompanydata.data_types.accounting.typed_refs import (
    AccountRef,
    CategoryRef,
    CustomerRef,
    ItemRef,
    ProjectRef,
    SalesOrderRef,
    TaxRateRef,
    TrackingCategoryRef,
)


class Tracking(BaseModel):
    categoryRefs: List[CategoryRef]
    projectRef: Optional[ProjectRef]
    customerRef: Optional[CustomerRef]
    isBilledTo: Optional[str]
    isRebilledTo: Optional[str]


class LineItem(BaseModel):
    description: Optional[str]
    unitAmount: float
    quantity: float
    discountAmount: Optional[float]
    subTotal: Optional[float]
    taxAmount: Optional[float]
    totalAmount: Optional[float]
    accountRef: Optional[AccountRef]
    discountPercentage: Optional[float]
    taxRateRef: Optional[TaxRateRef]
    itemRef: Optional[ItemRef]
    trackingCategoryRefs: List[TrackingCategoryRef]
    tracking: Optional[Tracking]
    isDirectIncome: bool


class PaymentAllocationPayment(BaseModel):
    id: Optional[str]
    note: Optional[str]
    reference: Optional[str]
    accountRef: Optional[AccountRef]
    currency: Optional[str]
    currencyRate: Optional[float]
    paidOnDate: datetime
    totalAmount: float


class PaymentAllocationAllocation(BaseModel):
    currency: Optional[str]
    currencyRate: Optional[float]
    allocatedOnDate: Optional[datetime]
    totalAmount: float


class PaymentAllocation(BaseModel):
    payment: PaymentAllocationPayment
    allocation: PaymentAllocationAllocation


class WithholdingTaxItem(BaseModel):
    name: Optional[str]
    amount: float


class Metadata(BaseModel):
    isDeleted: bool


class Invoice(BaseModel):
    id: str
    invoiceNumber: Optional[str]
    customerRef: CustomerRef
    salesOrderRefs: List[SalesOrderRef]
    issueDate: datetime
    dueDate: Optional[datetime]
    modifiedDate: Optional[datetime]
    sourceModifiedDate: Optional[datetime]
    paidOnDate: Optional[datetime]
    currency: Optional[str]
    currencyRate: float
    lineItems: List[LineItem]
    paymentAllocations: List[PaymentAllocation]
    withholdingTax: List[WithholdingTaxItem]
    totalDiscount: float
    subTotal: float
    additionalTaxAmount: float
    additionalTaxPercentage: float
    totalTaxAmount: float
    totalAmount: float
    amountDue: float
    discountPercentage: Optional[float]
    status: Optional[str]
    note: Optional[str]
    metadata: Optional[Metadata]
