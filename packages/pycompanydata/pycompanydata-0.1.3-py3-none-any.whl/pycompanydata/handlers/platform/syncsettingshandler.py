from pycompanydata.data_types.platform.syncsettings import SyncSettings
from pycompanydata.handlers.base import BaseHandler


class SyncSettingHandler(BaseHandler):
    def get_sync_settings(self, company_id: str) -> SyncSettings:
        result = self.client.get(self.path + company_id + "/syncSettings")
        sync_settings = SyncSettings(**result)
        return sync_settings
