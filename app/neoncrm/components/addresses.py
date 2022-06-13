"""NeonCRM API v2 Python Client"""

from app.neoncrm import util
from app.neoncrm.components import base


class Addresses(base.BaseComponent):
    """Component dealing with all account related matters"""

    def create(self, **kwargs):
        return self.post_request(
            "/addresses", json=kwargs)


    def update(self, **kwargs):
        util.require_keys(kwargs, 'accountId')
        return self.put_request(
            "/addresses/{}".format(kwargs['addressId']), json=kwargs
        )

    def get(self, **kwargs):
        util.require_keys(kwargs, 'addressId')
        return self.get_request(
            "/addresses/{}".format(kwargs['addressId']))
