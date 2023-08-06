from typing import List, Optional

from pydantic import BaseModel

from ..pagination import PaginatedResponse


class DataSetMetadata(BaseModel):
    id: str
    companyId: str
    connectionId: str
    dataType: Optional[str] = None
    status: str
    errorMessage: Optional[str] = None
    requested: str
    completed: Optional[str] = None
    progress: int
    isCompleted: bool
    isErrored: bool
    validationinformationUrl: Optional[str] = None


class DataSetMetaDataPaginatedResponse(PaginatedResponse):
    results: List[DataSetMetadata] = []
