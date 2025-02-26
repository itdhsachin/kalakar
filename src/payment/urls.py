from django.urls import path
from .views import create_payment, payment_callback

urlpatterns = [
    path("initiate/", create_payment, name="initiate_payment"),
    path("callback/", payment_callback, name="payment_callback"),
]
