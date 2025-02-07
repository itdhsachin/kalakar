from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random
import string

def generate_password(length=8):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

@csrf_exempt
def payment_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            payment_info = data.get("payload", {}).get("payment", {}).get("entity", {})

            email = payment_info.get("email")  # Extract email from webhook
            name = payment_info.get("name")
            amount = payment_info.get("amount") / 100  # Convert paise to INR

            if email:
                username = email.split("@")[0]  # Create a username from email
                password = generate_password()  # Generate a random password

                # ✅ Create User in Django
                user, created = User.objects.get_or_create(username=username, email=email)
                if created:
                    user.set_password(password)
                    user.save()

                    # ✅ Send Email with Credentials
                    subject = "Your Account Credentials"
                    message = f"Hello {name},\n\nYour account has been created.\nUsername: {username}\nPassword: {password}\n\nLogin here: http://yourwebsite.com/login"

                    send_mail(subject, message, "your-email@example.com", [email], fail_silently=False)

                    return JsonResponse({"message": "User created and email sent!"}, status=201)
                else:
                    return JsonResponse({"message": "User already exists!"}, status=200)

            return JsonResponse({"error": "Email is required"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
