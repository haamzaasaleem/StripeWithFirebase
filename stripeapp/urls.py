from django.urls import path, include
from .views import *
urlpatterns = [
    path('', custom_webhook),
]
