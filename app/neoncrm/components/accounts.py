"""NeonCRM API v2 Python Client"""

from app.neoncrm import util
from app.neoncrm.components import base


class Accounts(base.BaseComponent):
    """Component dealing with all account related matters"""

    def create(self, **kwargs):
        util.require_keys(kwargs, 'individualAccount')
        if kwargs.get('start_time'):
            kwargs['start_time'] = util.date_to_str(kwargs['start_time'])
        return self.post_request(
            "/accounts", json=kwargs)


    def update(self, **kwargs):
        util.require_keys(kwargs, 'accountId', 'inidividualAccount')
        return self.patch_request(
            "/accounts/" + kwargs.pop('accountId'), json=kwargs
        )

    def search(self, **kwargs):
        util.require_keys(
            kwargs,
            [
                'outputFields',
                'pagination',
                'searchFields'
            ]
        )
        return self.post_request('/accounts/search', json=kwargs)

    def get_search_fields(self, **kwargs):
        return self.get_request("/accounts/search/searchFields", params=kwargs)

    def get_output_fields(self, **kwargs):
        return self.get_request("/accounts/search/outputFields", params=kwargs)

