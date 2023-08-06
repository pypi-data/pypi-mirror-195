import datetime
from typing import List, Optional

from pydantic import BaseModel


class Address(BaseModel):
    type: Optional[str]
    line1: Optional[str]
    line2: Optional[str]
    city: Optional[str]
    region: Optional[str]
    country: Optional[str]
    postalCode: Optional[str]


class Supplier(BaseModel):
    id: Optional[str]
    supplierName: Optional[str]
    contactName: Optional[str]
    emailAddress: Optional[str]
    phone: Optional[str]
    addresses: Optional[List[Address]]
    registrationNumber: Optional[str]
    taxNumber: Optional[str]
    status: Optional[str]
    modifiedDate: Optional[datetime.datetime]
    sourceModifiedDate: Optional[datetime.datetime]
    defaultCurrency: Optional[str]
