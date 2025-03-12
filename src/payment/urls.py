from django.urls import path

from .views import payment_callback

urlpatterns = [
    path("callback/", payment_callback, name="payment_callback"),
]
