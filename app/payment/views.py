import os
import json
import stripe

from flask import Blueprint, request, session, url_for
from flask import render_template, redirect, jsonify
from flask_login import current_user, login_required

from config import csrf

from app.salesforce import Contact, Opportunity, Recurring_Donation

from app.neon import Account, Donation

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

payment = Blueprint("payment", __name__)


@payment.route('/config', methods=['GET'])
def get_config():
    return jsonify(
        {
            'publishableKey': os.getenv('STRIPE_PUBLISHABLE_KEY'),
            'productID': os.getenv('STRIPE_PRODUCT_ID')
        }
    )


@payment.route('/create-customer', methods=['POST'])
@csrf.exempt
def create_customer():
    # Reads paymentlication/json and returns a response
    data = json.loads(request.data)
    try:
        q = stripe.Customer.search(query="email:'{}'".format(data['email']))
        if len(q.data) > 0:
            customer = stripe.Customer.retrieve(q.data[0].id) 
        else:
            # Create a new customer object
            customer = stripe.Customer.create(**data)
        response = jsonify(customer=customer)

        # We're simulating authentication here by storing the ID of the customer
        # in a cookie.
        response.set_cookie('customer', customer.id)

        return response
    except Exception as e:
        return jsonify(error=str(e)), 403


@payment.route('/create-payment-intent', methods=['POST'])
@csrf.exempt
def create_payment():
    data = json.loads(request.data)

    # Each payment method type has support for different currencies. In order to
    # support many payment method types and several currencies, this server
    # endpoint accepts both the payment method type and the currency as
    # parameters.
    #
    # Some example payment method types include `card`, `ideal`, and `alipay`.
    payment_method_type = data['paymentMethodType']
    amount = int(data['amount']) * 100
    currency = data['currency']
    customer = data['customer']
    metadata = data['metadata']

    # Create a PaymentIntent with the amount, currency, and a payment method type.
    #
    # See the documentation [0] for the full list of supported parameters.
    #
    # [0] https://stripe.com/docs/api/payment_intents/create
    params = {
        'payment_method_types': [payment_method_type],
        'amount': amount,
        'currency': currency,
        'customer': customer,
        'metadata': metadata
    }

    # If this is for an ACSS payment, we add payment_method_options
    # to create the Mandate. This is not required if you're not accepting
    # ACSS (Pre-authorized debit in Canada).
    if payment_method_type == 'acss_debit':
        params['payment_method_options'] = {
            'acss_debit': {
                'mandate_options': {
                    'payment_schedule': 'sporadic',
                    'transaction_type': 'personal'
                }
            }
        }


    try:
        payment_intent = stripe.PaymentIntent.create(**params)

        # Send PaymentIntent details to the front end.
        return jsonify({'clientSecret': payment_intent.client_secret})
    except stripe.error.StripeError as e:
        return jsonify({'error': {'message': str(e)}}), 400
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400


@payment.route('/create-subscription', methods=['POST'])
@csrf.exempt
def create_subscription():
    data = json.loads(request.data)
    data['items'][0]['price_data']['unit_amount'] = int(data['items'][0]['price_data']['unit_amount']) * 100

    try:
        subscription = stripe.Subscription.create(
            **data,
            payment_behavior='default_incomplete',
            expand=['latest_invoice.payment_intent'],
        )

        return jsonify(
            subscriptionId=subscription.id, 
            clientSecret=subscription.latest_invoice.payment_intent.client_secret
        )

    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400

@payment.route('/update-donation', methods=['POST'])
@csrf.exempt
def update_donation():
    data = json.loads(request.data)

    try:
        payment = stripe.PaymentIntent.retrieve(data['payment_intent'])
        if payment['status'] == 'succeeded':
            return jsonify({'success':True}), 200
        else:
            return jsonify({'error': {'message': 'Payment could not be completed. Please try again another time.'}}), 400


    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400


@payment.route('/create-checkout-session', methods=['POST'])
@csrf.exempt
def create_checkout_session():
    data = json.loads(request.data)

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [customer_email] - lets you prefill the email input in the form
        # For full details see https:#stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param

        basket = data['basket']

        if basket['mode'] == 'payment':
            basket['lineItems'][0]['price_data']['product'] = 'prod_KZZCERmZQIMyrK'

        else:
            basket['lineItems'][0]['price_data']['product'] = 'prod_JwCRtGdq0IeCS9'

        if len(basket['lineItems']) > 1 or basket.get('shippingAddressCollection'):
            checkout_session = stripe.checkout.Session.create(
                success_url=basket['successUrl'],
                cancel_url=basket['cancelUrl'],
                payment_method_types=['card'],
                mode=basket['mode'],
                shipping_address_collection={'allowed_countries' : basket['shippingAddressCollection']['allowedCountries']},
                line_items=basket['lineItems'],
                metadata=basket['metadata']
            )
        else:
            checkout_session = stripe.checkout.Session.create(
                success_url=basket['successUrl'],
                cancel_url=basket['cancelUrl'],
                payment_method_types=['card'],
                mode=basket['mode'],
                line_items=basket['lineItems'],
                metadata=basket['metadata']
            )
        print(data['basket'])

        return jsonify({'sessionId': checkout_session['id']})

    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400

@payment.route('/update-user-premiums', methods=['POST'])
@csrf.exempt
def update_user_premiums():
    data = json.loads(request.data)

    try:
        email = data['email']
        premiums = data['premiums']
        city = data['city']
        country = data['country']
        line1 = data['line1']
        line2 = data['line2']
        postal_code = data['postal_code']

        address = {
            'city' : city,
            'line1' : line1,
            'line2' : line2,
            'country' : country,
            'postal_code' : postal_code
        }

        if 'bulletin' in premiums:
            Account(email, bulletin=True, address=address)

            return jsonify({'status': 'succeded'}), 200

    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400


#@payment.route('/subscriptions', methods=['GET'])
#def get_subscriptions():



@payment.route('/every_webhook', methods=['POST'])
def receive_every_webhook():
    webhook_secret = os.getenv('EVERY_ORG_WEBHOOK_SECRET')
    request_data = json.loads(request.data)

    charge_id = request_data['chargeId']
    partnerDonation_id = request_data['partnerDonationId']
    first_name = request_data['firstNmae']
    last_name = request_data['lastName']
    email = request_data['email']
    
    # Request a shared secret from every.org to decrypt incoming data stream
    pass


@payment.route('/webhook', methods=['POST'])
@csrf.exempt
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    # New customer
    if event_type == 'customer.created':
        try:
            email = data_object['email']
            name = data_object['name']
            method = data_object['metadata']['method']
            origin = 'Stripe Donation Module'
            address = data_object['address']

            Account(email, name, method, origin)

            Contact(email, name, address)

            note = email + " has created an account and is in the CRM"

        except Exception as e:
            return jsonify({'error': {'message': str(e)}}), 400
        

    # Invoice Payment Success
    if event_type == 'invoice.payment_succeeded':
        if data_object['billing_reason'] == 'subscription_create':
            subscription_id = data_object['subscription']
            charge_id = data_object['charge']
            payment_intent_id = data_object['payment_intent']

            charge = stripe.Charge.retrieve(charge_id)
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            card = charge.payment_method_details.card

            subscription = stripe.Subscription.retrieve(subscription_id)
            recurring = subscription.items.data[0].price.recurring.interval

            recurring_donation_id = Recurring_Donation(email, amount, card, recurring).id

            stripe.Subscription.modify(
                subscription_id,
                default_payment_method=payment_intent.payment_method,
                metadata={'recurring_donation_id' : recurring_donation_id}
            )

            note = 'Payment method attached to subscription'

    if event_type == 'payment_intent.succeeded':
        try:
            charge = data_object['charges']['data'][0]['id']
            stripe.Charge.modify(charge, metadata=data_object['metadata'])
            note = 'Metadata applied to charge'

        except Exception as e:
            return jsonify({'error': {'message': str(e)}}), 400
        
    if event_type == 'charge.succeeded':
        try:
            allocation = data_object['metadata']['allocation']
            amount = int(data_object['amount']) / 100
            campaign = data_object['metadata']['allocation']
            charge = data_object['id']
            customer = stripe.Customer.retrieve(data_object['customer'])
            method = data_object['metadata']['method']
            source = 'Stripe Checkout'
            referrer = data_object['metadata'].get('referrer')
            if data_object.get('invoice'):
                invoice_id = data_object['invoice']
                invoice = stripe.Invoice.retrieve(invoice_id)
                subscription_id = invoice['subscription']
                subscription = stripe.Subscription.retrieve(subscription_id)
                fund = {'id' : 19}
                interval = subscription.items.data[0].price.recurring.interval
                if interval == 'month':
                    recurring = 'Monthly'
                elif interval == 'year':
                    recurring = 'Yearly'
            else:
                fund = {'id' : 1}
                recurring = None

            redirect = data_object['metadata'].get('redirect')
            if redirect:
                page = "www.maps.org/" + redirect
            else:
                page = data_object['metadata']['donation_page']

            donation = Donation(
                allocation, amount, campaign, charge, customer, fund, method,
                source, page=page, recurring=recurring, referrer=referrer
            )
            donation.update()

            email = customer['email']
            tender_type = 'Stripe'
            source = 'MAPSi'
            page = 'Test Page'

            if not recurring:
                Opportunity(email, amount, tender_type, amount, source, page, charge, recurring=recurring)

            note = 'Donation successfully imported to the CRM'

        except Exception as e:
            return jsonify({'error': {'message': str(e)}}), 400
        

    return jsonify(success=True, note=note)