"""NeonCRM API v2 Python Client"""

from neoncrm import util
from neoncrm.components import base

class Properties(base.BaseComponent):
    """Component dealing with all payment related matters"""

    def get_countries(self):
        return self.get_request("/properties/countries")

    def get_funds(self):
        return self.get_request("/properties/funds")

    def get_purposes(self):
        return self.get_request("/properties/purposes")

    def get_sources(self):
        return self.get_request("/properties/sources")
        
    def get_stateProvinces(self):
    	return self.get_request("properties/stateProvinces")    
