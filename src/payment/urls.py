from django.urls import path
from .views import payment_webhook

urlpatterns = [
    path("webhook/", payment_webhook, name="payment_webhook"),
]