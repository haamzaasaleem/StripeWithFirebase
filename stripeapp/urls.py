from django.urls import path, include
from .views import *
urlpatterns = [
    path('webhook/', custom_webhook),
]
