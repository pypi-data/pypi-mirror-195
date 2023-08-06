import datetime
from typing import List, Optional

from pydantic import BaseModel

from pycompanydata.data_types.pagination import PaginatedResponse


class ValidDatatypeLink(BaseModel):
    property: Optional[str]
    links: Optional[List[str]]


class Account(BaseModel):
    id: Optional[str]
    nominalCode: Optional[str]
    name: Optional[str]
    description: Optional[str]
    fullyQualifiedCategory: Optional[str]
    fullyQualifiedName: Optional[str]
    currency: Optional[str]
    currentBalance: Optional[int]
    type: str
    status: str
    isBankAccount: bool
    modifiedDate: Optional[datetime.datetime]
    sourceModifiedDate: Optional[datetime.datetime]
    validDatatypeLinks: Optional[List[ValidDatatypeLink]]


class AccountsPaginatedResponse(PaginatedResponse):
    results: List[Account] = []
