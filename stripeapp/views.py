from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import stripe
from .utils import update_stripe_data,database,downgrade_firebase_user
from core.settings import STRIPE_ENDPOINT_SECRET,STRIPE_SECRET_KEY,DOMAIN_URL


# Create checkout
@csrf_exempt
def create_checkout_session(request):

    if request.method == 'POST':
        domain_url = DOMAIN_URL
        stripe.api_key = STRIPE_SECRET_KEY
        data = json.loads(request.body)
        try:
            customer_id = data.get('cus_id')
            price_id = data.get('price_id')
            checkout_session = stripe.checkout.Session.create(
                success_url= domain_url + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url= domain_url + 'cancelled/',
                payment_method_types=['card'],
                customer=customer_id,
                mode='subscription',
                line_items=[{

                    'price': price_id,
                    'quantity': 1
                }
                ],
            )
            return JsonResponse ({"checkout_url":checkout_session.url})
        except Exception as e:
            return JsonResponse({'error': str(e)})


# catching events
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
        if event['type'] == 'customer.subscription.trial_will_end':
            print("trial will end in 3 days")

        if event['type'] == 'customer.subscription.updated':
                session = event['data']['object']
                customer = session['customer']
                collection = database.collection('subscriptions').where('customerId', '==', customer).get()
                if collection:
                    update_stripe_data(collection,session)
        if event['type'] == 'checkout.session.completed':
            print("Completed")
            session = event['data']['object']

        return HttpResponse(status=200)



def downgrade_subscription(request):
    payload = request.body
    body = json.loads(payload)
    customer = body.get('cus_id')
    firebase_data = database.collection('subscriptions').where('customerId', '==', customer).get()
    downgrade_firebase_user(firebase_data)
    return JsonResponse({'message':'success'},safe=False)