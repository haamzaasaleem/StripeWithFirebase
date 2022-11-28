from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('create_checkout_session/', create_checkout_session,name="create-checkout"),
    path('downgrade/subscription', downgrade_subscription,name="downgrade-subscription"),
    path('user/challenges', csrf_exempt(user_challenges),name="user-challenges"),
    path('webhook/', custom_webhook,name="webhook-listener"),
]
