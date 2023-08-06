import datetime
from typing import List, Optional

from pydantic import BaseModel


class SyncSetting(BaseModel):
    dataType: Optional[str] = None
    fetchOnFirstLink: bool
    syncSchedule: int
    syncOrder: int
    syncFromUtc: Optional[datetime.datetime] = None
    syncFromWindow: Optional[int] = None
    monthsToSync: Optional[int] = None


class SyncSettings(BaseModel):

    companyId: str
    settings: Optional[List[SyncSetting]] = None
    overridesDefaults: bool
