"""NeonCRM API v2 Python Client"""

from neoncrm import util
from neoncrm.components import base

class Payments(base.BaseComponent):
    """Component dealing with all payment related matters"""

    def get_tenders(self):
        return self.get_request("/payments/tenders")
