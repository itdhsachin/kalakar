"""Defines URL patterns for payment-related views."""

from django.urls import path
from payment.views import PaymentWebhook  # ✅ Absolute import

urlpatterns = [
    path("webhook/", PaymentWebhook.as_view(), name="payment-webhook"),
]
