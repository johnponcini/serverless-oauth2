"""NeonCRM API v2 Python Client"""

from app.neoncrm import util
from app.neoncrm.components import base

class Campaigns(base.BaseComponent):
    """Component dealing with all campaign-related matters"""

    def get_campaigns(self):
        return self.get_request("/campaigns")

