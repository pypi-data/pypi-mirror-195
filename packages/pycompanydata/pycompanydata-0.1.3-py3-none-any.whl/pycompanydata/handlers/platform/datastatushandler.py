from pycompanydata.data_types.platform.datastatus import DataStatus
from pycompanydata.handlers.base import BaseHandler


class DataStatusHandler(BaseHandler):
    def get_company_data_status(self, company_id: str) -> DataStatus:
        result = self.client.get(self.path + company_id + "/dataStatus")
        return DataStatus(**result)
