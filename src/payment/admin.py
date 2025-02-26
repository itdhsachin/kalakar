from django.contrib import admin
from payment.models import CoursePrice, Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "email", "phone", "amount", "currency", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("email", "phone", "order_id", "payment_id")
@admin.register(CoursePrice)
class CoursePriceAdmin(admin.ModelAdmin):
    list_display = ("id", "courseName", "Date", "amount", "active")
    list_filter = ("active",)
    actions = ["make_active"]

    def make_active(self, request, queryset):
        """Admin action to set a price as active."""
        if queryset.count() > 1:
            self.message_user(request, "Please select only one price to activate.", level="error")
        else:
            CoursePrice.objects.filter(active=True).update(active=False)  # Deactivate all
            queryset.update(active=True)  # Activate selected price
            self.message_user(request, "Selected price is now active.")

    make_active.short_description = "Set selected price as active."
