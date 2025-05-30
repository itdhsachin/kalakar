import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Student, User
from accounts.utils import generate_password, send_html_email
from payment.models import Payment
from assessment.models import StudentCompetition
from courses.models import Course, Enrollment
import requests
from decouple import config
from django.shortcuts import get_object_or_404
import logging
import os
import urllib.parse
from django.utils import timezone
# import razorpay

from django.conf import settings

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
            existing_user = User.objects.filter(email=email).first()


            status = payment_info.get("status")
            # print("Status:", status)
            notes = payment_info.get("notes", {})
            # first_name = notes.get("first_name", "").strip()
            # last_name = notes.get("last_name", "").strip()
            # pincode = notes.get("pincode", "").strip()
            course_id = notes.get("course_id", "").strip()
            course = get_object_or_404(Course, id=course_id)

            print("course id =" , course_id)
            

            if not email:
                return JsonResponse(
                    {"status": "error", "message": "Email not found"},
                    status=400,
                )

            if status == "captured":

                
                # if the user is not exists
                try:
                    if existing_user:
                        # Create enrollment for existing user
                        try:
                            Enrollment.objects.create(
                            user=existing_user,
                            course=course,
                            created_by=existing_user,
                            enrollment_date = timezone.now(),
                            target_end_date=course.enroll_end_date,
                            state=True,
                            )

                            email_context = {
                            # "name": fullname,
                            "name": "User",
                            }

                            send_html_email(
                                subject="Thank you for your purchase!",
                                recipient_list=[email],
                                template="../templates/payment/emails/purchase.html",
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
                                        {"name": "username", "value": email}
                                    ],
                                    "template_name": "new_course2",
                                    "broadcast_name": "new_course2_200520251846",
                                }
                            )
                            headers = {
                                "content-type": "application/json-patch+json",
                                "Authorization": WATI_API_KEY,
                            }

                            response = requests.post(
                                whatsapp_url, data=payload, headers=headers
                            )
                            logging.info(f"WhatsApp payload: {payload}")
                            # print(response.text)
                            # SMS API details
                            api_username = 'irarangoli.trans'
                            api_password = 'k6p7s'
                            password = "123456"

                            sms_text = urllib.parse.quote(
                                f"Welcome to KalaGuru by Ira Rangoli Arts! Login URL: https://kalagurubyirarangoliarts.com/accounts/login/ "
                                f"Username: {email} Password: {password} Login and check 'My Course' for video. Team, Ira Rangoli Arts"
                            )

                            sms_url = (
                                f"https://api.smartping.ai/fe/api/v1/send?"
                                f"username={api_username}&password={api_password}&unicode=false&from=IRAART&to={phone}"
                                f"&dltPrincipalEntityId=1701174490170334566&dltContentId=1707174532032556467&text={sms_text}"
                            )

                            # sresponse = requests.get(sms_url)
                            
                            # logging.info(f"SMS API Response: {sms_url}")
                        except Exception as e:
                            logging.error(f"Failed to create enrollment: {e}")
                        return JsonResponse(
                        {"status": "success", "message": "Enrollment created for existing user"}
                        )
                    else:
                        password = generate_password()
                        user = User.objects.create_user(
                            username=email,
                            # first_name=first_name,
                            # last_name=last_name,
                            email=email,
                            phone=phone,
                            password=password,
                        )
                        user.is_student = True
                        user.save()
                        # fullname = f"{first_name} {last_name}"
                        # print(fullname)
                        Student.objects.create(
                            student=user,
                            # full_name=fullname, 
                            # pincode=pincode
                        )
                        if amount > 0:
                            newAmount = amount /100
                        Payment.objects.create(
                            user=user,
                            order_id=razorpay_order_id,
                            payment_id=razorpay_payment_id,
                            amount=newAmount,
                            email=email,
                            phone=phone,
                            status=status,
                            # pincode=pincode,
                        )
                        try:
                            Enrollment.objects.create(
                            user=user,
                            course=course,
                            created_by=user,
                            enrollment_date = timezone.now(),
                            target_end_date=course.enroll_end_date,
                            state=True,
                            )
                        except Exception as e:
                            logging.error(f"Failed to create enrollment: {e}")

                        email_context = {
                            # "name": fullname,
                            "name": "Hi User",
                            "username": email,
                            "password": password,
                            "Amount": amount / 100,
                            "start_date" : "17 June",
                            "end_date" : "10 July"
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
                                    {"name": "username", "value": email},
                                    {"name": "password", "value": password}
                                ],
                                "template_name": "new_uer_signup",
                                "broadcast_name": "new_uer_signup_200320251433",
                            }
                        )
                        headers = {
                            "content-type": "application/json-patch+json",
                            "Authorization": WATI_API_KEY,
                        }

                        response = requests.post(
                            whatsapp_url, data=payload, headers=headers
                        )
                        logging.info(f"WhatsApp payload: {payload}")
                        # print(response.text)

                        # SMS API details
                        api_username = 'irarangoli.trans'
                        api_password = 'k6p7s'

                        sms_text = urllib.parse.quote(
                            f"Welcome to KalaGuru by Ira Rangoli Arts! Login URL: https://kalagurubyirarangoliarts.com/accounts/login/ "
                            f"Username: {email} Password: {password} Login and check 'My Course' for video. Team, Ira Rangoli Arts"
                        )

                        sms_url = (
                            f"https://api.smartping.ai/fe/api/v1/send?"
                            f"username={api_username}&password={api_password}&unicode=false&from=IRAART&to={phone}"
                            f"&dltPrincipalEntityId=1701174490170334566&dltContentId=1707174532032556467&text={sms_text}"
                        )

                        sresponse = requests.get(sms_url)
                        
                        logging.info(f"SMS API Response: {sms_url}")
                        
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

# try:
#     razorpay_client = razorpay.Client(auth=(config("RAZORPAY_KEY_ID"), config("RAZORPAY_KEY_SECRET")))
# except Exception as e:

#     logging.info(e)
# logging.info(razorpay_client)

# def test_payment_url(request):
#         """View to test fetching Razorpay payment URL."""
#         payment_id = request.GET.get("payment_id")  # Get payment ID from query params

#         if not payment_id:
#             return JsonResponse({"error": "Payment ID is required"}, status=400)

#         try:
#             payment = razorpay_client.payment.fetch(payment_id)
#             order_id = payment.get("order_id")

#             if order_id:
#                 order = razorpay_client.order.fetch(order_id)
#                 receipt = order.get("receipt", "Unknown")

#                 # Log and return response
#                 logging.info(f"Test Payment URL for {payment_id}: {receipt}")
#                 return JsonResponse({"payment_id": payment_id, "payment_url": receipt})

#             logging.warning(f"No order found for payment ID: {payment_id}")
#             return JsonResponse({"error": "No order found for this payment ID"}, status=404)

#         except Exception as e:
#             logging.error(f"Error fetching payment URL for {payment_id}: {str(e)}")
#             return JsonResponse({"error": "Failed to fetch payment URL", "details": str(e)}, status=500)
