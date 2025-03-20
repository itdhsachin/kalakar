from django.urls import path

from coupon import views

urlpatterns = [
    path("coupon/", views.coupon, name="coupon"),
    path("list-coupon/", views.list_coupons, name="coupon"),
    path("check-coupon/", views.check_coupon, name="check_coupon"),
]
