"""Signal handlers for the accounts app.

This module contains the post-save signal handler for the accounts application,
which handles the creation of new user accounts.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Student, Teacher
from accounts.utils import (
    generate_lecturer_credentials,
    generate_student_credentials,
)


def post_save_account_receiver(instance=None, created=False, *args, **kwargs):
    """Send email notification after creating a new user account.

    This function generates credentials for new student and lecturer accounts
    and saves the user instance with the generated username and password.

    Args:
        instance (User): The user instance that was created or updated.
        created (bool): Indicates whether the user instance was created.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """
    if created:
        if instance.is_student:
            username, password = generate_student_credentials()
            instance.username = username
            instance.set_password(password)
            instance.save()
            # Send email with the generated credentials
            # send_new_account_email(instance, password)

        if instance.is_lecturer:
            username, password = generate_lecturer_credentials()
            instance.username = username
            instance.set_password(password)
            instance.save()

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    """ Automatically create a Student entry if a User with is_student=True is created """
    if created and instance.is_student:  # Check if the user is newly created and is a student
        Student.objects.create(student=instance)

@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    """Automatically create a Teacher entry if a User with is_lecturer=True is created."""
    if created and instance.is_lecturer:  # Check if the user is newly created and is a lecturer
        Teacher.objects.create(teacher=instance)