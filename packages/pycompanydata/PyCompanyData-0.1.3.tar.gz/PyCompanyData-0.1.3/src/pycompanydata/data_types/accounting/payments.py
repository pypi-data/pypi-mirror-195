from __future__ import annotations

import datetime
from typing import List, Optional

from pydantic import BaseModel

from pycompanydata.data_types.accounting.typed_refs import (
    AccountRef,
    CustomerRef,
    PaymentMethodRef,
)


class Link(BaseModel):
    # TODO 'type' is actually  an enum [ Unknown, Unlinked, Invoice, CreditNote, Other,
    # Refund, Payment, PaymentOnAccount, ManualJournal, Discount ]
    type: str
    id: Optional[str]
    amount: Optional[int]
    currencyRate: Optional[int]


class Line(BaseModel):
    amount: int
    links: Optional[List[Link]]
    allocatedOnDate: Optional[datetime.datetime]


class Payment(BaseModel):
    id: Optional[str]
    customerRef: Optional[CustomerRef]
    accountRef: AccountRef
    paymentMethodRef: Optional[PaymentMethodRef]
    totalAmount: int
    currency: str
    currencyRate: Optional[int]
    date: datetime.datetime
    note: Optional[str]
    lines: Optional[List[Line]]
    modifiedDate: Optional[datetime.datetime]
    sourceModifiedDate: Optional[datetime.datetime]
    reference: Optional[str]
