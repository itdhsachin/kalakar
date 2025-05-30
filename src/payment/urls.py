from django.urls import path

from .views import payment_callback

urlpatterns = [
    path("callback/", payment_callback, name="payment_callback"),
    # path("test-payment-url/", test_payment_url, name="test_payment_url"),
]
