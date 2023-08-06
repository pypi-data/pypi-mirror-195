import datetime
from typing import List, Optional

from pydantic import BaseModel


class DataConnectionError(BaseModel):
    statusCode: Optional[str] = None
    erroredOnUtc: Optional[datetime.datetime] = None
    statusText: Optional[str] = None
    errorMessage: Optional[str] = None


class DataConnection(BaseModel):
    id: str
    integrationId: str
    sourceId: str
    platformName: str
    linkUrl: str
    status: Optional[str] = None
    created: Optional[datetime.datetime] = None
    sourceType: Optional[str] = None
    lastSync: Optional[datetime.datetime] = None
    DataConnectionErrors: Optional[List[DataConnectionError]] = None
