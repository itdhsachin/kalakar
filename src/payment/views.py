"""Views for handling payment-related operations, including webhooks and email notifications."""

import json
import threading
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from accounts.models import User
from accounts.utils import create_valid_username, generate_password

"""Module for handling payments in the application."""


class EmailThread(threading.Thread):
    """A thread to handle email sending asynchronously."""

    def __init__(
        self, subject, plain_message, from_email, recipient_list, html_message
    ):
        """Initialize the email thread with the required email details.

        Args:
            subject (str): The subject of the email.
            plain_message (str): The plain text content of the email.
            from_email (str): The sender's email address.
            recipient_list (list): List of recipient email addresses.
            html_message (str): The HTML version of the email content.
        """
        self.subject = subject
        self.plain_message = plain_message
        self.from_email = from_email
        self.recipient_list = recipient_list
        self.html_message = html_message
        threading.Thread.__init__(self)

    def run(self):
        """Execute the thread's task of sending an email."""
        send_mail(
            self.subject,
            self.plain_message,
            self.from_email,
            self.recipient_list,
            html_message=self.html_message,
        )


@method_decorator(csrf_exempt, name="dispatch")
class PaymentWebhook(View):
    """Handle incoming payment webhooks."""

    def post(self, request, *args, **kwargs):
        """Process a POST request from the payment gateway webhook."""
        try:
            data = json.loads(request.body)
            payment_info = (
                data.get("payload", {}).get("payment", {}).get("entity", {})
            )

            email = payment_info.get("email")  # Extract email from webhook
            name = payment_info.get("name")
            amount = (
                payment_info.get("amount", 0) / 100
            )  # Convert paise to INR safely

            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)

            base_username = email.split("@")[0]
            username = create_valid_username(base_username)
            password = generate_password()  # Generate a random password

            # ✅ Create User in Django
            user, created = User.objects.get_or_create(
                username=username, email=email
            )
            if created:
                user.set_password(password)
                user.save()

                # ✅ Send Email with Credentials (Using EmailThread)
                subject = "Your Account Credentials"
                context = {
                    "name": name,
                    "username": username,
                    "password": password,
                    "Amount": amount,
                }
                html_message = render_to_string(
                    "emails/account_credentials.html", context
                )
                plain_message = strip_tags(
                    html_message
                )  # Convert HTML to plain text

                EmailThread(
                    subject,
                    plain_message,
                    "your-email@example.com",
                    [email],
                    html_message,
                ).start()

                return JsonResponse(
                    {"message": "User created and email sent!"}, status=201
                )
            else:
                return JsonResponse(
                    {"message": "User already exists!"}, status=200
                )

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        """Handle GET requests and return an error response."""
        return JsonResponse({"error": "Invalid request"}, status=400)
