import razorpay
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from accounts.utils import generate_student_credentials, send_html_email
import json
import razorpay
from accounts.models import Student, User
from payment.models import CoursePrice

def create_payment(request):
    if request.method == "POST":
        firstName = request.POST.get("first_name")
        lastName = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        amount = CoursePrice.get_current_price() * 100
        currency = "INR"

        payment_data = {
            "amount": amount,
            "currency": currency,
            "payment_capture": 1,
            "notes": {"first_name": firstName, "last_name": lastName,"email": email, "phone": phone}
        }

        order = client.order.create(data=payment_data)
        request.session["razorpay_order_id"] = order["id"]


        return JsonResponse({"order_id": order["id"], "amount": amount, "currency": currency})

    return render(request, "payment/initiate_payment.html", {"razorpay_key": settings.RAZORPAY_KEY_ID})


@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            razorpay_payment_id = data.get("razorpay_payment_id")
            razorpay_order_id = data.get("razorpay_order_id")
            razorpay_signature = data.get("razorpay_signature")

            stored_order_id = request.session.get("razorpay_order_id")

            if stored_order_id != razorpay_order_id:
                return JsonResponse({"status": "error", "message": "Order ID mismatch"}, status=400)

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            try:
                client.utility.verify_payment_signature({
                    "razorpay_order_id": razorpay_order_id,
                    "razorpay_payment_id": razorpay_payment_id,
                    "razorpay_signature": razorpay_signature
                })

                order = client.order.fetch(razorpay_order_id)

                # print(order)
                firstName = order["notes"]["first_name"]
                lastName = order["notes"]["last_name"]
                email = order["notes"]["email"]
                phone = order["notes"]["phone"]
                status = order['status']
                amount = order['amount']

                # payment, created = Payment.objects.get_or_create(
                #     order_id=razorpay_order_id,
                #     defaults={
                #         "payment_id": razorpay_payment_id,
                #         "amount": amount,
                #         "email": email,
                #         "phone": phone,
                #         "status": status
                #     },
                # )
                # if not created:
                #     # If payment exists, update it
                #     payment.payment_id = razorpay_payment_id
                #     payment.status = status
                #     payment.save()


                if User.objects.filter(email=email).exists():
                    # print("The email id is already registered..")
                    return JsonResponse({"status": "success", "message": "User already exists"})

                if status == 'paid' :
                    try:
                        username, password = generate_student_credentials()
                        # print(f"Generated Username: {username}, Password: {password}")

                        user = User.objects.create_user(username=username,first_name=firstName, last_name = lastName ,email=email,phone=phone, password=password)
                        user.is_student = True 
                        user.save()
                        
                        Student.objects.create(student=user)
                        # payment.user = user  # Link payment to user
                        # payment.save()
                        # print(f"User Created Successfully: {username} - {email}")

                        email_context = {
                            "name": firstName + " " + lastName,
                            "username": username,
                            "password": password,
                            "Amount": amount / 100
                        }

                        send_html_email(
                            subject="Your Account Credentials - Payment Received",
                            recipient_list=[email],
                            template="../templates/payment/emails/account_credentials.html",
                            context=email_context
                        )
                        return JsonResponse({"status": "success", "message": "User created successfully", "username": username, "password": password})

                    except Exception as e:
                        # print("User Creation Failed:", str(e))
                        return JsonResponse({"status": "error", "message": "User creation failed", "error": str(e)}, status=500)

            except razorpay.errors.SignatureVerificationError:
                return JsonResponse({"status": "error", "message": "Invalid payment signature"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
        except Exception as e:
            # print("Unexpected Error:", str(e))
            return JsonResponse({"status": "error", "message": "Unexpected error", "error": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
