"""NeonCRM API v2 Python Client"""

from neoncrm import util
from neoncrm.components import base


class Orders(base.BaseComponent):
    """Component dealing with all account related matters"""

    def create(self, **kwargs):
        util.require_keys(kwargs, 'individualAccount')
        if kwargs.get('start_time'):
            kwargs['start_time'] = util.date_to_str(kwargs['start_time'])
        return self.post_request(
            "/accounts", json=kwargs)


    def update(self, **kwargs):
        util.require_keys(kwargs, 'accountId', 'inidividualAccount')
        return self.put_request(
            "/accounts/" + kwargs['accountId'], json=kwargs
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
        return self.post_request('/orders/search', json=kwargs)

    def get_search_fields(self, **kwargs):
        return self.get_request("/orders/search/searchFields", params=kwargs)

    def get_output_fields(self, **kwargs):
        return self.get_request("/orders/search/outputFields", params=kwargs)

    def retrieve(self, **kwargs):
        util.require_keys(kwargs, 'meetingId')
        return self.get_request(
            "/meetings/{}".format(kwargs['meetingId']), params=kwargs)
