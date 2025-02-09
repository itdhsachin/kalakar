import random
import string
import re
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from accounts.models import User

def generate_password(length=8):
    """Generate a random password with letters, digits, and special characters."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choices(characters, k=length))

def generate_random_username():
    """Generate a random valid username according to UnicodeUsernameValidator regex."""
    regex = UnicodeUsernameValidator.regex
    while True:
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if re.match(regex, username):
            return username

def create_valid_username(base_username):
    """Create a valid and unique username based on the base username."""
    validator = UnicodeUsernameValidator()
    username = base_username
    attempts = 0

    while attempts < 10:
        try:
            validator(username)
            if not User.objects.filter(username=username).exists():
                return username
        except ValidationError:
            pass
        # Append random digits to make the username unique
        username = f"{base_username}_{random.randint(1000, 9999)}"
        attempts += 1

    # If unique username creation failed 10 times, generate a random valid username
    return generate_random_username()