import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Student, User
from accounts.utils import generate_password, send_html_email
from payment.models import Payment
import requests
from decouple import config
import logging
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "razorpay_webhook.log")

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,  # Save log in 'logs/razorpay_webhook.log'
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # print(data)
            logging.info("Received Webhook Data: %s", json.dumps(data, indent=4))

            if data.get("event") != "payment.captured":
                return JsonResponse(
                    {"status": "ignored", "message": "Event not relevant"},
                    status=200,
                )

            payment_info = data.get("payload", {}).get("payment", {}).get("entity", {})

            razorpay_payment_id = payment_info.get("id")
            razorpay_order_id = payment_info.get("order_id")
            email = payment_info.get("email")
            phone = payment_info.get("contact")
            amount = payment_info.get("amount", 0)

            # print("Amount:", amount)
            if not (0 <= amount <= 5000):
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Invalid payment amount.",
                    },
                    status=400,
                )

            status = payment_info.get("status")
            # print("Status:", status)
            notes = payment_info.get("notes", {})
            first_name = notes.get("first_name", "").strip()
            last_name = notes.get("last_name", "").strip()
            pincode = notes.get("pincode", "").strip()

            if not email:
                return JsonResponse(
                    {"status": "error", "message": "Email not found"},
                    status=400,
                )

            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                return JsonResponse(
                    {"status": "success", "message": "User already exists"}
                )
            if status == "captured":
                try:
                    password = generate_password()
                    user = User.objects.create_user(
                        username=email,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=phone,
                        password=password,
                    )
                    user.is_student = True
                    user.save()
                    fullname = f"{first_name} {last_name}"
                    # print(fullname)
                    Student.objects.create(
                        student=user, full_name=fullname, pincode=pincode
                    )

                    Payment.objects.create(
                        user=user,
                        order_id=razorpay_order_id,
                        payment_id=razorpay_payment_id,
                        amount=amount,
                        email=email,
                        phone=phone,
                        status=status,
                        pincode=pincode,
                    )

                    email_context = {
                        "name": fullname,
                        "username": email,
                        "password": password,
                        "Amount": amount / 100,
                    }

                    send_html_email(
                        subject="Your Account Credentials - Payment Received",
                        recipient_list=[email],
                        template="../templates/payment/emails/account_credentials.html",
                        context=email_context,
                    )
                    if phone.startswith("+"):
                        whatsAppPhone = phone[1:]
                        # print(whatsAppPhone)
                    WATI_API_URL = config("WATI_API_URL")
                    WATI_API_KEY = config("WATI_API_KEY")
                    whatsapp_url = f"{WATI_API_URL}?whatsappNumber={whatsAppPhone}"

                    payload = json.dumps(
                        {
                            "parameters": [
                                {"name": "name", "value": fullname}
                                # {"name": "username", "value": email},
                                # {"name": "password", "value": password}
                            ],
                            "template_name": "new_chat_v1",
                            "broadcast_name": "new_chat_v1_170320251849",
                        }
                    )
                    headers = {
                        "content-type": "application/json-patch+json",
                        "Authorization": WATI_API_KEY,
                    }

                    response = requests.post(
                        whatsapp_url, data=payload, headers=headers
                    )

                    print(response.text)
                    return JsonResponse(
                        {
                            "status": "success",
                            "message": "User created successfully",
                            "username": email,
                        }
                    )

                except Exception as e:
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": "User creation failed",
                            "error": str(e),
                        },
                        status=500,
                    )

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"}, status=400
            )
        except Exception as e:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Unexpected error",
                    "error": str(e),
                },
                status=500,
            )

    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )
