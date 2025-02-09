from django.shortcuts import render
from accounts.models import User
from accounts.utils import generate_password, generate_random_username, create_valid_username
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
import threading

class EmailThread(threading.Thread):
    def __init__(self, subject, plain_message, from_email, recipient_list, html_message):
        self.subject = subject
        self.plain_message = plain_message
        self.from_email = from_email
        self.recipient_list = recipient_list
        self.html_message = html_message
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, self.plain_message, self.from_email, self.recipient_list, html_message=self.html_message)

@method_decorator(csrf_exempt, name='dispatch')
class PaymentWebhook(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            payment_info = data.get("payload", {}).get("payment", {}).get("entity", {})

            email = payment_info.get("email")  # Extract email from webhook
            name = payment_info.get("name")
            amount = payment_info.get("amount", 0) / 100  # Convert paise to INR safely

            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)

            base_username = email.split("@")[0]
            username = create_valid_username(base_username)
            password = generate_password()  # Generate a random password

            # ✅ Create User in Django
            user, created = User.objects.get_or_create(username=username, email=email)
            if created:
                user.set_password(password)
                user.save()

                # ✅ Send Email with Credentials (Using EmailThread)
                subject = "Your Account Credentials"
                context = {"name": name, "username": username, "password": password, "Amount":amount}
                html_message = render_to_string("emails/account_credentials.html", context)
                plain_message = strip_tags(html_message)  # Convert HTML to plain text
                
                EmailThread(subject, plain_message, "your-email@example.com", [email], html_message).start()

                return JsonResponse({"message": "User created and email sent!"}, status=201)
            else:
                return JsonResponse({"message": "User already exists!"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        return JsonResponse({"error": "Invalid request"}, status=400)
