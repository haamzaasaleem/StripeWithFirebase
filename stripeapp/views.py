from pathlib import Path
import firebase_admin
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import credentials
from firebase_admin import firestore
from pathlib import Path
import datetime
import json
import stripe
from .utils import update_stripe_data

BASE_DIR = Path(__file__).resolve().parent.parent
cred = credentials.Certificate(f"{BASE_DIR}/firebase.json")
firebase_admin.initialize_app(cred)
database = firestore.client()

STRIPE_SECRET_KEY = "sk_test_51I4Tz3HF3TKtlSd4rkSraIW9rTRdY4z1MAk4hHvYMa4u2joLcIA342oao8l3vVzUdENFIJvCarNIAB9Wwmn0Teen00d7OSke72"
STRIPE_ENDPOINT_SECRET="whsec_9c20158d2e7f9361eca8b7cfca54d2c8781128a9c3811b1766be8f9dea790722"

@csrf_exempt
def custom_webhook(request):
    event = None
    payload = request.body
    body = json.loads(payload)
    session = body['data']['object']
    if STRIPE_ENDPOINT_SECRET:
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=payload, sig_header=sig_header, secret=STRIPE_ENDPOINT_SECRET
            )
        except stripe.error.SignatureVerificationError as e:
            print(':warning:  Webhook signature verification failed.' + str(e))
            return HttpResponse(status=400)
        # if event['type'] == 'customer.subscription.created':
        #         session = event['data']['object']
        #         print("end in CREATED:::",session)
        #         print("end in CREATED:::",session['current_period_end'])
        #         print("start in CREATED:::",session['current_period_start'])
        #         print("interval in CREATED:::",session['interval'])
        #         # print("customer_id:::",customer_id)
        if event['type'] == 'customer.subscription.created' or event['type'] == 'customer.subscription.updated':
                session = event['data']['object']
                customer = session['customer']
                collection = database.collection('subscriptions').where('customerId', '==', customer).get()
                if collection:
                    update_stripe_data(collection,session)
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
        return HttpResponse(status=200)