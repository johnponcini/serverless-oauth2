"""NeonCRM API v2 Python Client"""

from app.neoncrm import util
from app.neoncrm.components import base


class CustomFields(base.BaseComponent):
    """Component dealing with all meeting related matters"""

    def list(self, **kwargs):
        util.require_keys(kwargs, 'userId')
        if kwargs.get('start_time'):
            kwargs['start_time'] = util.date_to_str(kwargs['start_time'])
        return self.get_request("/users/{}/meetings".format(kwargs['userId']))

    def create(self, **kwargs):
        util.require_keys(kwargs, 'individualAccount')
        if kwargs.get('start_time'):
            kwargs['start_time'] = util.date_to_str(kwargs['start_time'])
        return self.post_request(
            "/accounts", json=kwargs)

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

    def get(self, **kwargs):
        util.require_keys(kwargs, ['category'])
        return self.get_request("/customFields", params=kwargs)

    def retrieve_past_participants(self, **kwargs):
        util.require_keys(kwargs, 'meetingUUID')
        return self.get_request(
            "/past_meetings/{}/particpants".format(kwargs['meetingUUID']), 
            params=kwargs)

