from django.urls import path
from .views import *
urlpatterns = [
    path('create_checkout_session/', create_checkout_session,name="create-checkout"),
    path('downgrade/subscription', downgrade_subscription,name="downgrade-subscription"),
    path('webhook/', custom_webhook,name="webhook-listener"),
]
