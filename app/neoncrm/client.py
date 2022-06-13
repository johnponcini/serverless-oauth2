from neoncrm import components, util


class NEON(util.API):

    BASE_URI = 'https://api.neoncrm.com/v2'

    def __init__(self, org_name, api_key, data_type='json', timeout=5):

        super().__init__(
            base_uri=NEON.BASE_URI,
            timeout=timeout
        )

        self.components = {
            'accounts' : components.accounts.Accounts(
                base_uri=NEON.BASE_URI,
                auth=(org_name, api_key)
            ),
            'addresses' : components.addresses.Addresses(
                base_uri=NEON.BASE_URI,
                auth=(org_name, api_key)
            ),
            'campaigns' : components.campaigns.Campaigns(
                base_uri=NEON.BASE_URI,
                auth=(org_name, api_key)
            ),
            'donations' : components.donations.Donations(
                base_uri=NEON.BASE_URI,
                auth=(org_name, api_key)
            ),
            'pledges' : components.pledges.Pledges(
                base_uri=NEON.BASE_URI,
                auth=(org_name, api_key)
            ),
            'memberships' : components.memberships.Memberships(
                base_uri=NEON.BASE_URI,
                auth=(org_name, api_key)
            ),
            'orders' : components.orders.Orders(
                base_uri=NEON.BASE_URI,
                auth=(org_name, api_key)
            ),
            'payments' : components.payments.Payments(
                base_uri=NEON.BASE_URI,
                auth=(org_name, api_key)
            ),
            'custom_fields' : components.custom_fields.CustomFields(
                base_uri=NEON.BASE_URI,
                auth=(org_name, api_key)
            ),
            'properties' : components.properties.Properties(
                base_uri=NEON.BASE_URI,
                auth=(org_name, api_key)
            ),
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    @property
    def accounts(self):
        return self.components.get('accounts')

    @property
    def addresses(self):
        return self.components.get('addresses')

    @property
    def campaigns(self):
        return self.components.get('campaigns')

    @property
    def donations(self):
        return self.components.get('donations')

    @property
    def pledges(self):
        return self.components.get('pledges')

    @property
    def memberships(self):
        return self.components.get('memberships')

    @property
    def orders(self):
        return self.components.get('orders')

    @property
    def payments(self):
        return self.components.get('payments')

    @property
    def custom_fields(self):
        return self.components.get('custom_fields')

    @property
    def properties(self):
        return self.components.get('properties')
