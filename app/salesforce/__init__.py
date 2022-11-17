from nameparser import HumanName
from datetime import datetime

from config import sf


class Contact:

    def __init__(self, email, name, address):
        '''
        Searches for an existing contact
        Creates a new contact if one does not exist
        '''
        self.contact = self.search(email)

        if not self.contact:
            if name:
                self.contact = self.create(email, HumanName(name), address)
            else:
                self.contact = self.create(email, name, address)


    def search(self, email):

        fields = [
            'Email', 'Company_Email__c', 'npe01__AlternateEmail__c', 
            'npe01__HomeEmail__c', 'npe01__WorkEmail__c', 
            'npe01__Preferred_Email__c'
        ]
        for field in fields:
            query = sf.query(
                "SELECT Id From Contact WHERE {} = '{}'".format(field, email)
            )
            if query.get('totalSize') == 0:
                continue
            else:
                try:
                    return sf.Contact.get(query['records'][0]['Id'])
                except:
                    continue
        return None

    def create(self, email, name, address):
        if name:
            first_name = name.first.capitalize()
            last_name = name.last.capitalize()
        else:
            first_name = '_'
            last_name = '_'
        if not first_name:
            first_name = '_'

        if not last_name:
            last_name = '_'
        
        if address:
            contact = sf.Contact.create(
                {
                    'FirstName' : first_name, 
                    'LastName' : last_name, 
                    'Email' : email,
                    'MailingCity' : address['city'],
                    'MailingCountry' : address['country'], 
                    'MailingStreet' : address['line1'],
                    'MailingPostalCode' : address['postal_code']
                }
            )   
        else:
            contact = sf.Contact.create(
                {
                    'FirstName' : first_name, 
                    'LastName' : last_name, 
                    'Email' : email
                }
            )
        return contact

    def id(self):
        return self.contact['id']


class Opportunity:
    '''
    A container to define donations and associated donation functions.
    '''
    def __init__(self, contact, amount, tender_type, source, page, charge_id, recurring_donation_id=None):
        '''
        '''
        account_id = contact['AccountId']

        if recurring_donation_id:
            self.opportunity = sf.Opportunity.create(
                {
                    'AccountId': account_id,
                    'Amount': amount,
                    'Name': 'Online Recurring Donation',
                    'Type': 'Donation',
                    'StageName': 'Closed Won',
                    'CloseDate': datetime.now().strftime('%Y-%m-%d'),
                    'RecordTypeId': 'Donation',
                    'Purpose__c': 'Unrestricted',
                    'Tender_Type__c': tender_type,
                    'Platform_Source__c': source,
                    'Donation_Page__c': page,
                    'Source_URL__c': page,
                    'Stripe_ID__c' : charge_id,
                    'npe03__Recurring_Donation__c': recurring_donation_id
                }
            )

        else:
            self.opportunity = sf.Opportunity.create(
                {
                    'AccountId': account_id,
                    'Amount': amount,
                    'Name': 'Online Recurring Donation',
                    'Type': 'Donation',
                    'StageName': 'Closed Won',
                    'CloseDate': datetime.now().strftime('%Y-%m-%d'),
                    'RecordTypeId': 'Donation',
                    'Purpose__c': 'Unrestricted',
                    'Tender_Type__c': tender_type,
                    'Platform_Source__c': source,
                    'Donation_Page__c': page,
                    'Source_URL__c': page,
                    'Stripe_ID__c' : charge_id,
                }
            )

    def id(self):
        return self.opportunity['id']

class Payment:
    '''
    A container to define payments.

    Amount: Same as Opportunity Amount
    Paid: True (assuming only posted items are coming through)
    Payment Created Date: Date of data entry
    Payment Received Date: Date donation was made
    Payment Posted Date: Date donation posted in Stripe (may be same as above)
    Tender Type: Payment Card
    Gateway Source: Stripe
    Gateway Payment ID: ID from Stripe (I can't remember if it's Charge ID, but whatever is helpful to Accounting)
    Cardholder Name: from Stripe
    Card Brand: from Stripe
    Card Expiration Month: from Stripe
    Card Expiration Year: from Stripe
    Payment Card Last 4 Digit: from Stripe
    '''
    def __init__(self, type, opportunity_id, amount, charge_id, card):
        '''
        '''
        if type == 'card':
            self.payment = sf.npe01__OppPayment__c.create(
                {
                    'npe01__Opportunity__c' : opportunity_id,
                    'npe01__Paid__c': True,
                    'npe01__Payment_Amount__c': amount,
                    'Payment_Created_Date__c': datetime.now().strftime('%Y-%m-%d'),
                    'npe01__Payment_Date__c': datetime.now().strftime('%Y-%m-%d'),
                    'Tender_Type__c': 'Payment Card',
                    'Gateway_Source__c': 'Stripe',
                    'npsp__Gateway_Payment_ID__c': charge_id,
                    'Card_Brand__c': card['brand'],
                    'npsp__Card_Expiration_Month__c': card['exp_month'],
                    'npsp__Card_Expiration_Year__c': card['exp_year'],
                    'npsp__Card_Last_4__c': card['last4']
                }
            )


class Recurring_Donation:
    '''
    A container to define recurring donations and associated functions.
    '''
    def __init__(self, email, amount, recurring):
        '''
        '''
        contact_id = sf.query("SELECT Id From Contact WHERE Email = '{}'".format(email))['records'][0]['Id']
        contact = sf.Contact.get(contact_id)
        account_id = contact['AccountId']
        installment_period = recurring.capitalize() + 'ly'

        self.recurring_donation = sf.npe03__Recurring_Donation__c.create(
            {
                'npe03__Organization__c': account_id,
                'npe03__Contact__c': contact_id,
                'npe03__Amount__c': amount,
                'Name': 'API',
                'npe03__Installment_Period__c': installment_period,
                'npe03__Date_Established__c': datetime.now().strftime('%Y-%m-%d'),
                'npsp__Day_of_Month__c': datetime.now().strftime('%-d')
            }
        )

    def id(self):
        return self.recurring_donation['id']
