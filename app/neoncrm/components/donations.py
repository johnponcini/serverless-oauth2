"""NeonCRM API v2 Python Client"""

from neoncrm import util
from neoncrm.components import base


class Donations(base.BaseComponent):
    """Component dealing with all donation-related matters"""

    def list(self, **kwargs):
        util.require_keys(kwargs, 'userId')
        if kwargs.get('start_time'):
            kwargs['start_time'] = util.date_to_str(kwargs['start_time'])
        return self.get_request("/users/{}/meetings".format(kwargs['userId']))

    def create(self, **kwargs):
        util.require_keys(
            kwargs,
            [
                'accountId',
                'acknowledgee',
                'amount',
                'date',
                'payments',
                'sendAcknowledgeEmail'
            ]
        )
        return self.post_request(
            '/donations', json=kwargs)

    def get(self, **kwargs):
        util.require_keys(kwargs, 'id')
        return self.get_request('/donations/{}'.format(kwargs['id']))

    def put(self, **kwargs):
        util.require_keys(
            kwargs,
            [
                'id',
                'accountId',
                'donorName',
                'amount',
                'date',
                'campaign',
                'fund',
                'purpose',
                'source',
                'anonymousType',
                'donorCoveredFeeFlag',
                'donationCustomFields'
            ],
        )
        return self.put_request('/donations/{}'.format(kwargs['id']), json=kwargs)

    def update_part(self, **kwargs):
        util.require_keys(kwargs, 'id')
        return self.patch_request('/donations/{}'.format(kwargs['id']), json=kwargs)

    def search(self, **kwargs):
        util.require_keys(
            kwargs,
            [
                'outputFields',
                'pagination',
                'searchFields'
            ]
        )
        return self.post_request('/donations/search', json=kwargs)

    def get_search_fields(self, **kwargs):
        return self.get_request('/donations/search/searchFields')

    def get_output_fields(self, **kwargs):
        return self.get_request('/donations/search/outputFields')

    def retrieve(self, **kwargs):
        util.require_keys(kwargs, 'meetingId')
        return self.get_request(
            "/meetings/{}".format(kwargs['meetingId']), params=kwargs)

    def update(self, **kwargs):
        util.require_keys(kwargs, 'meetingId')
        if kwargs.get('start_time'):
            kwargs['start_time'] = util.date_to_str(kwargs['start_time'])
        return self.patch_request(
            "/meetings/{}".format(kwargs['meetingId']), data=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, 'meetingId')
        return self.delete_request(
            "/meetings/{}".format(kwargs['meetingId']), params=kwargs)

    def end(self, **kwargs):
        util.require_keys(kwargs, 'meetingId')
        data = {'action' : 'end'}
        return self.put_request(
            "/meetings/{}/status".format(kwargs['meetingId']), data=data)

    def retrieve_past_participants(self, **kwargs):
        util.require_keys(kwargs, 'meetingUUID')
        return self.get_request(
            "/past_meetings/{}/particpants".format(kwargs['meetingUUID']), 
            params=kwargs)
