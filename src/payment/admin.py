from django.contrib import admin

from payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "email",
        "phone",
        "amount",
        "currency",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("email", "phone", "order_id", "payment_id")

    def get_readonly_fields(self, request, obj=None):
        """Make user field read-only in the admin panel"""
        if obj:  # Only make it read-only for existing objects
            return ["user"]
        return []
