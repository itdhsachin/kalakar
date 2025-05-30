"""Utility functions and classes for the accounts app.

This module contains functions for generating IDs, sending emails,
and the EmailThread class for sending emails asynchronously.
"""

import random
import string
import threading
from datetime import datetime
# import razorpay

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_html_email(subject, recipient_list, template, context):
    """Send an HTML email.

    Args:
        subject (str): The subject of the email.
        recipient_list (list): List of recipient email addresses.
        template (str): The path to the HTML template.
        context (dict): The context to render the template with.
    """
    # Render the HTML template
    html_message = render_to_string(template, context)

    # Generate plain text version of the email (optional)
    plain_message = strip_tags(html_message)

    # Send the email
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,  # Use DEFAULT_FROM_EMAIL
        recipient_list,
        fail_silently=False,
        html_message=html_message,
    )


def generate_password():
    """Generate a random password for a user.

    Returns:
        str: The generated password.
    """
    # return get_user_model().objects.make_random_password()
    chars =  string.digits 
    length = 7
    return "".join(random.choice(chars) for _ in range(length))


def generate_student_id():
    """Generate a unique ID for a student.

    Returns:
        str: The generated student ID.
    """
    registered_year = datetime.now().strftime("%Y")
    students_count = get_user_model().objects.filter(is_student=True).count()
    return f"{settings.STUDENT_ID_PREFIX}-{registered_year}-{students_count}"


def generate_lecturer_id():
    """Generate a unique ID for a lecturer.

    Returns:
        str: The generated lecturer ID.
    """
    registered_year = datetime.now().strftime("%Y")
    lecturers_count = get_user_model().objects.filter(is_lecturer=True).count()
    return f"{settings.LECTURER_ID_PREFIX}-{registered_year}-{lecturers_count}"


def generate_student_credentials():
    """Generate credentials (ID and password) for a student.

    Returns:
        tuple: The generated student ID and password.
    """
    return generate_student_id(), generate_password()


def generate_lecturer_credentials():
    """Generate credentials (ID and password) for a lecturer.

    Returns:
        tuple: The generated lecturer ID and password.
    """
    return generate_lecturer_id(), generate_password()


class EmailThread(threading.Thread):
    """Thread for sending emails asynchronously.

    Args:
        subject (str): The subject of the email.
        recipient_list (list): List of recipient email addresses.
        template_name (str): The path to the HTML template.
        context (dict): The context to render the template with.
    """

    def __init__(self, subject, recipient_list, template_name, context):
        """Intializer."""
        self.subject = subject
        self.recipient_list = recipient_list
        self.template_name = template_name
        self.context = context
        threading.Thread.__init__(self)

    def run(self):
        """Send the HTML email when the thread is run."""
        send_html_email(
            subject=self.subject,
            recipient_list=self.recipient_list,
            template=self.template_name,
            context=self.context,
        )


def send_new_account_email(user, password):
    """Send an account confirmation email to a new user.

    Args:
        user (User): The user to send the email to.
        password (str): The user's password.
    """
    if user.is_student:
        template_name = "accounts/email/new_student_account_confirmation.html"
    else:
        template_name = "accounts/email/new_lecturer_account_confirmation.html"
    email = {
        "subject": "Your Kalakar account confirmation and credentials",
        "recipient_list": [user.email],
        "template_name": template_name,
        "context": {"user": user, "password": password},
    }
    EmailThread(**email).start()

# def get_user_attendance_percentage(user, course):
#     """Calculate user's lesson completion percentage in a course."""
#     total_lessons = 2  
#     completed_lessons = LessonTrack.objects.filter(user=user, course=course, completed_at__isnull=False).count()

#     if total_lessons == 0:
#         return 0  

#     return (completed_lessons / total_lessons) * 100

# razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
# def get_payment_url(payment_id):
#     """Retrieve Payment URL using Razorpay Payment ID"""
#     try:
#         payment = razorpay_client.payment.fetch(payment_id)
#         order_id = payment.get("order_id")

#         if order_id:
#             order = razorpay_client.order.fetch(order_id)
#             receipt = order.get("receipt", "Unknown")
#             return receipt  # Return the URL directly
        
#         return None  # Return None if no order is found

#     except Exception as e:
#         return f"Error fetching payment URL: {str(e)}" 
