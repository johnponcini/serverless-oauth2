"""NeonCRM API v2 Python Client"""

from neoncrm import util
from neoncrm.components import base


class Pledges(base.BaseComponent):
    """Component dealing with all donations related matters"""

    def get_pledge_payments(self, **kwargs):
        util.require_keys(kwargs, 'pledge_id')
        return self.get_request('/pledges/{}/pledgePayments'.format(kwargs['pledge_id']))

    def get_pledge_payment(self, **kwargs):
        util.require_keys(kwargs, ['pledge_id', 'payment_id'])
        return self.get_request('/pledges/{}/pledgePayments/{}'.format(kwargs['pledge_id'], kwargs['payment_id']))

#    def post_pledge_payment(self, **kwargs):
#        util.require_keys(kwargs, 'pledge_id')
#        return self.post_request('/pledges/{}/pledgePayments'.format(kwargs['pledge_id']))
