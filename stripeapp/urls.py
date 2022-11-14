from django.urls import path, include
from .views import *
urlpatterns = [
    path('', StripeViewset.as_view()),
]
