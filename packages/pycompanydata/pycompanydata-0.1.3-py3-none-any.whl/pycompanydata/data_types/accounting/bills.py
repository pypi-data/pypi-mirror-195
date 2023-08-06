from typing import List, Optional

from pydantic import BaseModel

from pycompanydata.data_types.accounting.typed_refs import (
    AccountRef,
    CategoryRef,
    CustomerRef,
    ItemRef,
    ProjectRef,
    PurchaseOrderRef,
    SupplierRef,
    TaxRateRef,
    TrackingCategoryRef,
)


class Tracking(BaseModel):
    categoryRefs: List[CategoryRef]
    customerRef: Optional[CustomerRef]
    projectRef: Optional[ProjectRef]
    isBilledTo: Optional[str]
    isRebilledTo: Optional[str]


class LineItem(BaseModel):
    description: Optional[str]
    unitAmount: Optional[int]
    quantity: Optional[int]
    discountAmount: Optional[int]
    subTotal: Optional[int]
    taxAmount: Optional[int]
    totalAmount: Optional[int]
    discountPercentage: Optional[int]
    accountRef: AccountRef
    taxRateRef: Optional[TaxRateRef]
    itemRef: Optional[ItemRef]
    trackingCategoryRefs: List[TrackingCategoryRef]
    tracking: Optional[Tracking]
    isDirectCost: Optional[bool]


class WithholdingTaxItem(BaseModel):
    name: Optional[str]
    amount: Optional[int]


class Payment(BaseModel):
    id: Optional[str]
    note: Optional[str]
    reference: Optional[str]
    accountRef: AccountRef
    currency: Optional[str]
    currencyRate: Optional[int]
    paidOnDate: Optional[str]
    totalAmount: Optional[int]


class Allocation(BaseModel):
    currency: Optional[str]
    currencyRate: Optional[int]
    allocatedOnDate: Optional[str]
    totalAmount: Optional[int]


class PaymentAllocation(BaseModel):
    payment: Payment
    allocation: Allocation


class Metadata(BaseModel):
    isDeleted: Optional[bool]


class Bill(BaseModel):
    id: Optional[str]
    reference: Optional[str]
    supplierRef: SupplierRef
    purchaseOrderRefs: List[PurchaseOrderRef]
    issueDate: Optional[str]
    dueDate: Optional[str]
    currency: Optional[str]
    currencyRate: Optional[int]
    lineItems: List[LineItem]
    withholdingTax: List[WithholdingTaxItem]
    status: Optional[str]
    subTotal: Optional[int]
    taxAmount: Optional[int]
    totalAmount: Optional[int]
    amountDue: Optional[int]
    modifiedDate: Optional[str]
    sourceModifiedDate: Optional[str]
    note: Optional[str]
    paymentAllocations: List[PaymentAllocation]
    metadata: Metadata
