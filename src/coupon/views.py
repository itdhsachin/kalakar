from django.http import JsonResponse
from django.shortcuts import render

from coupon.models import Coupons


def coupon(request):
    """This will take to the coupon page."""
    return render(request, "coupon/coupon.html")


def list_coupons():
    """This will return all the list of the coupons."""
    coupons = Coupons.objects.values_list("coupon_code", flat=True)
    return JsonResponse({"coupons": list(coupons)})


def check_coupon(request):
    """THis is for the checking purpose of coupons exits in our db."""
    coupon_code = request.GET.get("coupon_code", "").strip()

    try:
        coupons = Coupons.objects.get(coupon_code=coupon_code)
        return JsonResponse(
            {
                "match": True,
                "message": "Coupon Code Matched!",
                "payment_link": coupons.payment_link,
            }
        )
    except Coupons.DoesNotExist:
        return JsonResponse({"match": False, "message": "Invalid Coupon Code!"})
