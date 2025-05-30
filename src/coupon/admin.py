"""Admin configuration for the accounts app.

This module contains the admin interface options for the Coupon models.
"""

from django.contrib import admin, messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import path
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from coupon.models import Coupons


class CouponsAdmin(admin.ModelAdmin):
    """Admin interface for Coupon."""

    list_display = [
        "user_id",
        "coupon_code",
        "payment_link",
         "price",
        "delete_button",
    ]
    # list_filter = ("user_id",)
    search_fields = ("coupon_code",)
    list_filter = ("user_id", "price")

    def delete_button(self, obj):
        """Generate a delete button for each  row."""
        return format_html(
            '<a class="button" style="color:white;" href="delete_coupon/?id={}">Delete</a>',
            obj.id,
        )

    delete_button.short_description = "Delete"

    def get_urls(self):
        """Add custom URL for deleting a coupon."""
        urls = super().get_urls()
        custom_urls = [
            path(
                "delete_coupon/",
                self.admin_site.admin_view(self.delete_coupon),
            ),
        ]
        return custom_urls + urls

    def delete_coupon(self, request):
        """Handles teacher deletion."""
        coupon_id = request.GET.get("id", None)

        if not coupon_id:
            messages.error(request, _("Coupon ID not provided."))
            return redirect("admin/coupon/coupons/")

        try:
            coupon = Coupons.objects.get(id=coupon_id)
            coupon.delete()
            messages.success(request, _("Coupon deleted successfully."))
        except ObjectDoesNotExist:
            messages.error(request, _("Coupon not found."))

        return redirect("/admin/coupon/coupons/")

    class Meta:
        """Meta class."""

        managed = True
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"


# Register models with admin panel
admin.site.register(Coupons, CouponsAdmin)
