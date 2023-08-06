from typing import Optional

from pydantic import BaseModel


class PurchaseOrderRef(BaseModel):
    id: Optional[str]
    purchaseOrderNumber: Optional[str]


class AccountRef(BaseModel):
    id: str
    name: Optional[str]


class SupplierRef(BaseModel):
    id: Optional[str]
    supplierName: Optional[str]


class CategoryRef(BaseModel):
    id: str
    name: Optional[str]


class BankAccountRef(BaseModel):
    id: Optional[str]
    name: Optional[str]


class CustomerRef(BaseModel):
    id: str
    companyName: Optional[str]


class ItemRef(BaseModel):
    id: str
    name: Optional[str]


class RecordRef(BaseModel):
    id: str
    dataType: Optional[str]


class ProjectRef(BaseModel):
    id: str
    name: Optional[str]


class SalesOrderRef(BaseModel):
    id: str
    dataType: Optional[str]


class TaxRateRef(BaseModel):
    id: str
    name: Optional[str]
    effectiveTaxRate: Optional[float]


class TrackingCategoryRef(BaseModel):
    id: str
    name: Optional[str]


class PaymentMethodRef(BaseModel):
    id: str
    name: Optional[str]
