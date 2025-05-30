from django.http import JsonResponse
from django.shortcuts import render
from coupon.models import Coupons

def coupon(request):
    """Render the coupon page."""
    return render(request, "coupon/coupon.html")


def list_coupons():
    """This will return all the list of the coupons."""
    coupons = Coupons.objects.values_list("coupon_code", flat=True)
    return JsonResponse({"coupons": list(coupons)})

def check_coupon(request):
    """Check if the coupon exists and return the corresponding payment link."""
    coupon_code = request.GET.get("coupon_code", "").strip()

    # Ensure default_coupon exists before accessing its attributes
    default_coupon = Coupons.objects.filter(coupon_code="default").first()

    if not default_coupon:
        return JsonResponse({
            "match": False,
            "message": "Default coupon not found.",
            "payment_link": ""  # Avoid error by returning an empty link
        })

    try:
        # Try to find a matching coupon
        coupon = Coupons.objects.get(coupon_code=coupon_code)
        return JsonResponse({
            "match": True,
            "message": "Referral Code Matched!",
            "payment_link": coupon.payment_link  # Use matched coupon's payment link
        })
    except Coupons.DoesNotExist:
        return JsonResponse({
            "match": False,
            "message": "Coupon not found.",
            "payment_link": default_coupon.payment_link  # Default link if no match
        })