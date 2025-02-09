from django.urls import path
from .views import PaymentWebhook

urlpatterns = [
    path('payment-webhook/', PaymentWebhook.as_view(), name='payment_webhook'),
]