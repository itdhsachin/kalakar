from django.conf import settings
from django.db import models


# Create your models here.
class Coupons(models.Model):
    """Model representing Coupons."""

    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="students_coupon",
    )
    coupon_code = models.TextField(max_length=50)
    payment_link = models.URLField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
