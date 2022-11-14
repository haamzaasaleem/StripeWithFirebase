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

BASE_DIR = Path(__file__).resolve().parent.parent
cred = credentials.Certificate(f"{BASE_DIR}/firebase.json")
firebase_admin.initialize_app(cred)
database = firestore.client()

STRIPE_SECRET_KEY = "sk_test_51KoniGKcrwcO2WsbAgrJCNGb4q6cuKbHXyXBmyZObyFs8oJffrPoIge9EEfDnpAnUx8CLESMd052Ym5vlsCS2ujk00VX1Q0iwp"
STRIPE_ENDPOINT_SECRET="whsec_8563e72f8cd66e0bd9d73ccda5fd0924dec3b605e3072593c54cde3295839e3f"

endpoint_secret=''
@csrf_exempt
def custom_webhook(request):
    print('webhook!')
    event = None
    payload = request.body
    body = json.loads(payload)
    print("payload:", body)

    if endpoint_secret:
        # print(request.headers['Stripe-Signature'])
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=payload, sig_header=sig_header, secret=STRIPE_ENDPOINT_SECRET
            )
            # print(event)
        except stripe.error.SignatureVerificationError as e:
            print(':warning:  Webhook signature verification failed.' + str(e))
            return HttpResponse(status=400)
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            print("session:", session['customer'])
            print("session:", session)

            # using the timestamp() function to convert datetime into epoch time
            epoch_time = datetime.datetime.now().timestamp()
            date_today = datetime.datetime.today().date()
            end_data = datetime.datetime.today().date() + datetime.timedelta(days=14)

            # printing the values
            print("Converted epoch time:", epoch_time)
            print("Today::", date_today)
            print("end_data::", end_data)
            docarray = []
            # cus_MncMBUmB7CozRw
            collection = database.collection('subscriptions').where('customerId', '==', 'cus_MNmFEiUZf00IOP').get()
            print("user history matched records", collection)
            # if
            for doc in collection:
                print("doc_id:", doc.id)
                currentTierData = {
                    'active': True,
                    'interval': 'Yearly',
                    'tier': "Goals By us 2",
                    'cancelled': False,
                    'endDate': str(end_data),
                    'interval': 'Yearly',
                    'startDate': str(date_today),
                    'tier': "Done by Us!"

                }
                trial_data = {
                    'active': True,
                    'current': {
                        'endDate': str(end_data),
                        'interval': "YEARLY",
                        'startDate': str(date_today),
                        'tier': 'NEW TIER'
                    }
                }
                if doc.to_dict()['currentTier']:
                    # doc.to_dict()['currentTier'].document(doc.id).update({'active':True})
                    database.collection('subscriptions').document(doc.id).update(
                        {"currentTier": currentTierData,
                         'trial': trial_data
                         })
        return HttpResponse(status=200)