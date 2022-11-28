from firebase_admin import credentials
from firebase_admin import firestore
from pathlib import Path
import firebase_admin
import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
cred = credentials.Certificate(f"{BASE_DIR}/firebase.json")
firebase_admin.initialize_app(cred)
database = firestore.client()


def update_stripe_data(firebase_data,stripe_data):

    plan_price_id = stripe_data['items']['data'][0]['plan']['id']
    plan_price_status = stripe_data['items']['data'][0]['plan']['active']
    interval = stripe_data['items']['data'][0]['plan']['interval']
    # trial_end = stripe_data['trial_end']
    # trial_start = stripe_data['trial_start']
    customer = stripe_data['customer']
    # customer = 'cus_MOAFiy530vs6VL'
    trial_start = stripe_data['current_period_start']
    trial_end = stripe_data['current_period_end']
    private_practice = False
    if plan_price_id == 'price_1L6UXTHF3TKtlSd4XYWVwgql' or plan_price_id == 'price_1L6UWRHF3TKtlSd4M4bflejF':
        tier = "Private Practice Solution"
        private_practice = True
        role = "Trainer"
        walkthrough = 'Private Practice Solution'
    if plan_price_id == 'price_1L6UWrHF3TKtlSd4kSJpY7wM' or plan_price_id == 'price_1L6UUxHF3TKtlSd4WTedWf1Q':
        tier = "Enterprise Solution"
        role = "Enterprise_Admin"
        walkthrough = 'Enterprise Solution'
    if plan_price_id == 'price_1LGNCfHF3TKtlSd43O9DqmVh' or plan_price_id == 'price_1LGNBtHF3TKtlSd47sKcCdr0':
        tier = "Coaching Solution"
        role = "Trainer"
        walkthrough = 'Coaching Solution'

    for doc in firebase_data:
        update_data = {}
        update_data['currentTier'] = {
            'active': plan_price_status,
            'interval': interval,
            'tier': tier,
            'cancelled': False,
            'endDate': trial_end,
            'interval': interval,
            'startDate': trial_start,
            'tier': tier
        }
        update_data['trial'] = {
            'active': plan_price_status,
            'current': {
                'endDate': trial_end,
                'interval':interval,
                'startDate': trial_start,
                'tier':tier
            }
        }
    database.collection('subscriptions').document(doc.id).update(update_data)

    # Updating the user
    user_data = database.collection('users').where("customerId", "==", customer).get()
    user_update_data = {}
    for data in user_data:
        data.to_dict()
        user_update_data ['active'] = True
        user_update_data ['createdTime'] = data.to_dict()['createdTime']
        user_update_data ['customerId'] = data.to_dict()['customerId']
        user_update_data ['email'] = data.to_dict()['email']
        user_update_data ['id'] = data.to_dict()['id']
        user_update_data ['role'] = role
        user_update_data ['interval'] = interval
        user_update_data ['lastLoginTime'] = data.to_dict()['lastLoginTime']
        user_update_data ['name'] = data.to_dict()['name']
        # user_update_data ['phone'] = data.to_dict()['phone'] #Not udpated
        user_update_data ['privatePractice'] = private_practice
        user_update_data ['state'] = data.to_dict()['state']
        user_update_data ['tier'] = tier
        if walkthrough == 'Enterprise Solution' :
            user_update_data['walkthrough'] = {
            'clientDetail': True,
            'clientEditor': True,
            'dashboard': True,
            'designer': True,
            'designerExercise': True,
            'shareWorkout': True,
            'workoutAssigner': True,
            'workoutAssignerCard': True,
            'workoutSummary': True,
        }
        if walkthrough == 'Private Practice Solution' :

            user_update_data['walkthrough'] = {
            'clientDetail': True,
            'clientEditor': False,
            'dashboard': False,
            'designer': False,
            'designerExercise': True,
            'shareWorkout': True,
            'workoutAssigner': True,
            'workoutAssignerCard': True,
            'workoutSummary': True,
        }

        if walkthrough == 'Coaching Solution' :

            user_update_data['walkthrough'] = {
            'clientDetail': True,
            'clientEditor': False,
            'dashboard': False,
            'designer': False,
            'designerExercise': False,
            'shareWorkout': True,
            'workoutAssigner': False,
            'workoutAssignerCard': True,
            'workoutSummary': True,
        }


    database.collection('users').document(doc.id).update(user_update_data)


def downgrade_firebase_user(firebase_data):

    for doc in firebase_data:
        update_subscription_data = {}
        current_tier_data = doc.to_dict()['currentTier']
        current_date = datetime.datetime.today()
        current_epoch = int(current_date.strftime("%s"))
        if current_tier_data['endDate'] == current_epoch :
            update_subscription_data['currentTier'] = {
            'active': False,
            'interval': 'free',
            'tier': 'Coaching Solution',
            'cancelled': False,
            'endDate': None,
            'startDate': None,
        }
            update_subscription_data['trial'] = {
                'active':False
            }
        else:
            if current_tier_data['cancelled'] == False:
                update_subscription_data['currentTier'] = {
                'active': True,
                'interval': current_tier_data['interval'],
                'tier': current_tier_data['tier'],
                'cancelled': True,
                'endDate': current_tier_data['endDate'],
                'interval': current_tier_data['interval'],
                'startDate': current_tier_data['startDate'],
                'tier': current_tier_data['tier']
            }
            else:
                update_subscription_data['currentTier'] = {
                'active': True,
                'interval': current_tier_data['interval'],
                'tier': current_tier_data['tier'],
                'cancelled': False,
                'endDate': current_tier_data['endDate'],
                'interval': current_tier_data['interval'],
                'startDate': current_tier_data['startDate'],
                'tier': current_tier_data['tier']
                }
        
    database.collection('subscriptions').document(doc.id).update(update_subscription_data)

def add_user_challenge(firebase_data,body):

    for doc in firebase_data:
        pass
    database.collection('users').document(doc.id).update({'challenges':{'0':{
        'id': body.get('id'),
        'name':body.get('name'),
        'picURL':body.get('picURL'),
        'preview':False,
        'value':body.get('value'),
    }},
    'programId':body.get('programId'),
    
    }
    
    
    
    
    )