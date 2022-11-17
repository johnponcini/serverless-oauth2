import os
import time
import json
import stripe

from flask import Blueprint, request, session, url_for
from flask import render_template, redirect, jsonify

from config import csrf

from app.salesforce import Contact, Opportunity, Recurring_Donation, Payment

from app.neon import Account, Donation

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

webhook = Blueprint("webhook", __name__)

@webhook.route('/', methods=['POST'])
@csrf.exempt
def webhook_received():
        # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    request_data = json.loads(request.data)

    # Define default fields
    tender_type = 'Stripe'
    source = 'MAPSi'
    page = 'Test Page'

    note = ''

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
        
    # Invoice Payment Success
    if event_type == 'invoice.payment_succeeded':
        try:
            # Retrieve the associated Subscription object
            subscription_id = data_object['subscription']
            subscription = stripe.Subscription.retrieve(subscription_id)

            # Retrieve the associated Charge
            charge_id = data_object['charge']
            charge = stripe.Charge.retrieve(charge_id)

            card = charge['payment_method_details']['card']
            # Retrive the associated Payment Intent
            payment_intent_id = data_object['payment_intent']
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            # Retrieve the associated Customer
            customer_id = charge['customer']
            customer = stripe.Customer.retrieve(customer_id)
            try:
                email = customer['email']
                name = customer.get('name')
                source = 'Stripe Checkout'
                origin = 'Stripe Donation Module'
                if customer['address']:
                    address = customer['address']
                else:
                    address = None

                Account(email, name, source, origin)

                contact = Contact(email, name, address).contact

                note += email + " has created an account and is in the CRM. "

            except Exception as e:
                return jsonify({'error': {'message': str(e)}}), 400
            # Extract fields
            email = customer['email']
            amount = int(charge['amount']) / 100
            recurring = subscription['items']['data'][0]['price']['recurring']['interval']

            if data_object['billing_reason'] == 'subscription_create':
                
                source = 'MAPSi'

                # Create a Recurring Donation
                #recurring_donation_id = Recurring_Donation(contact, amount, recurring).id()
                recurring_donation_id = None

                # Create an Opportunity and attach it to the newly created Recurring Donation
                opportunity = Opportunity(contact, amount, tender_type, source, page, charge_id, recurring_donation_id)
                Payment(opportunity.id(), amount, charge_id, card)

                # Update the Subscription object with the default payment method and recurring donation ID
                stripe.Subscription.modify(
                    subscription_id,
                    default_payment_method=payment_intent.payment_method,
                    metadata={'recurring_donation_id' : recurring_donation_id}
                )
            
                note += 'Payment method attached to subscription, Recurring Donation and Opportunity created.'

            else:
                source = 'MAPSi'
                # Extract the Recurring Donation ID from the Subscription metadata
                try:
                    recurring_donation_id = subscription['metadata']['recurring_donation_id']
                except:
                    recurring_donation_id = Recurring_Donation(email, amount, recurring).id()
                    stripe.Subscription.modify(
                        subscription_id,
                        metadata={'recurring_donation_id' : recurring_donation_id}
                    )

                # Create the Opportunity
                recurring_donation_id = None
                opportunity = Opportunity(contact, amount, tender_type, source, page, charge_id, recurring_donation_id)
                Payment(opportunity.id(), amount, charge_id, card)

                note += 'Opportunity created for Recurring Donation.'
            
            # Attach Subscription metadata to the Charge
            stripe.Charge.modify(charge_id, metadata=subscription['metadata'])

        except Exception as e:
            return jsonify({'error': {'message': str(e)}}), 400

    if event_type == 'payment_intent.succeeded':
        try:
            charge = data_object['charges']['data'][0]['id']
            stripe.Charge.modify(charge, metadata=data_object['metadata'])
            note = 'Metadata applied to charge'

        except Exception as e:
            return jsonify({'error': {'message': str(e)}}), 400
        
    if event_type == 'charge.succeeded':
        try:
            charge_id = data_object['id']
            amount = int(data_object['amount']) / 100
            card = data_object['payment_method_details']['card']
            customer = stripe.Customer.retrieve(data_object['customer'])
            try:
                email = customer['email']
                name = customer['name']
                source = 'Stripe Checkout'
                origin = 'Stripe Donation Module'
                if customer['address']:
                    address = customer['address']
                else:
                    address = None

                Account(email, name, source, origin)

                contact = Contact(email, name, address).contact

                note += email + " has created an account and is in the CRM. "

            except Exception as e:
                return jsonify({'error': {'message': str(e)}}), 400

            source = 'Stripe Checkout'
            if data_object.get('invoice'):                
                invoice_id = data_object['invoice']
                invoice = stripe.Invoice.retrieve(invoice_id)
                subscription_id = invoice['subscription']
                subscription = stripe.Subscription.retrieve(subscription_id)
                try:
                    allocation = subscription['metadata']['allocation']
                    campaign = subscription['metadata']['campaign']
                    method = subscription['metadata']['method']
                except:
                    allocation = 'unrestricted'
                    campaign = 'general purpose'
                    method = 'online'
                referrer = subscription['metadata'].get('referrer')
                redirect = subscription['metadata'].get('redirect')
                if redirect:
                    page = "www.maps.org/" + redirect
                else:
                    try:
                        page = payment_intent['metadata']['donation_page']
                    except:
                        page = 'https://maps.org'
                fund = {'id' : 19}
                interval = subscription['items']['data'][0]['price']['recurring']['interval']
                if interval == 'month':
                    recurring = 'Monthly'
                elif interval == 'year':
                    recurring = 'Yearly'
            else:
                try:
                    payment_intent_id = data_object['payment_intent']
                    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                    try:
                        allocation = payment_intent['metadata']['allocation']
                        campaign = payment_intent['metadata']['campaign']
                        method = payment_intent['metadata']['method']
                    except:
                        allocation = 'unrestricted'
                        campaign = 'general purpose'
                        method = 'online'                     
                    referrer = payment_intent['metadata'].get('referrer')
                    redirect = payment_intent['metadata'].get('redirect')
                    if redirect:
                        page = "www.maps.org/" + redirect
                    else:
                        try:
                            page = payment_intent['metadata']['donation_page']
                        except:
                            page = 'https://maps.org'
                    fund = {'id' : 1}
                    recurring = None
                    if not data_object['description'] or 'Order' not in data_object['description']:
                        opportunity = Opportunity(contact, amount, tender_type, 'MAPSi', page, charge_id)
                        Payment(opportunity.id(), amount, charge_id, card)
                        
                except Exception as e:
                    return jsonify({'error': {'message': str(e)}}), 400

            if not data_object['description'] or 'Order' not in data_object['description']:
                donation = Donation(
                    allocation, amount, campaign, charge_id, customer, fund, method,
                    source, page=page, recurring=recurring, referrer=referrer
                )
                donation.update()

                note += 'Donation successfully imported to the CRM'
            else:
                note += 'Store Orders not currently imported via webhooks to the CRM.'

        except Exception as e:
            return jsonify({'error': {'message': str(e)}}), 400

    return jsonify(success=True, note=note)


@webhook.route('/every_org', methods=['POST'])
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


