from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar("T")


class LinkHref(BaseModel):
    href: Optional[str] = None


class PaginationLinks(BaseModel):
    self: Optional[LinkHref] = None
    current: Optional[LinkHref] = None
    next: Optional[LinkHref] = None
    previous: Optional[LinkHref] = None


class PaginatedResponse(GenericModel, Generic[T]):
    results: List[T]
    pageNumber: Optional[int] = None
    pageSize: Optional[int] = None
    totalResults: Optional[int] = None
    links: PaginationLinks = Field(None, alias="_links")
