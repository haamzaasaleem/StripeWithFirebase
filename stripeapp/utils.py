from stripeapp import views


def update_stripe_data(firebase_data,stripe_data):

    plan_price_id = stripe_data['items']['data'][0]['plan']['id']
    plan_price_status = stripe_data['items']['data'][0]['plan']['active']
    interval = stripe_data['items']['data'][0]['plan']['interval']
    trial_end = stripe_data['trial_end']
    trial_start = stripe_data['trial_start']
    customer = stripe_data['customer']
    if plan_price_id == 'price_1L6UXTHF3TKtlSd4XYWVwgql' or plan_price_id == 'price_1L6UWRHF3TKtlSd4M4bflejF':
        tier = "Private Practice Solution"
    if plan_price_id == 'price_1L6UWrHF3TKtlSd4kSJpY7wM' or plan_price_id == 'price_1L6UUxHF3TKtlSd4WTedWf1Q':
        tier = "Enterprise Solution"
    if plan_price_id == 'price_1LGNCfHF3TKtlSd43O9DqmVh' or plan_price_id == 'price_1LGNBtHF3TKtlSd47sKcCdr0':
        tier = "TEST Solution"
    for doc in firebase_data:
        currentTierData = {
            'active': plan_price_status,
            'interval': interval,
            'tier': tier,
            'cancelled': False,
            'endDate': trial_end,
            'interval': interval,
            'startDate': trial_start,
            'tier': tier
        }
        trial_data = {
            'active': plan_price_status,
            'current': {
                'endDate': trial_end,
                'interval':interval,
                'startDate': trial_start,
                'tier':tier
            }
        }
    views.database.collection('subscriptions').document(doc.id).update(
                        {"currentTier": currentTierData,
                         'trial': trial_data
                         })