import datetime
from django.db import models
from accounts.models import User

"""Defines database models for the payment system."""
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("created", "Created"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order_id = models.CharField(max_length=255, unique=True)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=10, default="INR")
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="created")
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.email} - {self.amount/100} {self.currency} - {self.status}"
class CoursePrice(models.Model):
    courseName = models.CharField(max_length=60, blank=True, null=True)
    Date = models.DateField(default=datetime.date.today)  
    amount = models.PositiveIntegerField()
    active = models.BooleanField(default=False)  # Only one should be active

    def __str__(self):
        return f"{self.courseName or 'Unnamed Course'} - ₹{self.amount} {'(Active)' if self.active else ''}"

    def save(self, *args, **kwargs):
        """Ensure only one active CoursePrice at a time."""
        if self.active:
            # Set all other active prices to False before saving
            CoursePrice.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    @staticmethod
    def get_current_price():
        """Get the currently active course price."""
        price = CoursePrice.objects.filter(active=True).first()
        if not price:
            raise ValueError("No active price set. Please add an active price in the admin panel.")
        return price.amount
