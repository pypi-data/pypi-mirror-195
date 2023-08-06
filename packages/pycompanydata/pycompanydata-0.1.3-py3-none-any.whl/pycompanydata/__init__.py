__version__ = "0.1.3"

from pycompanydata.clients.accounting_client import AccountingClient
from pycompanydata.clients.platform_client import PlatformClient


class Codat(AccountingClient, PlatformClient):
    """The main class which acts as an interface to the Codat API."""

    pass
