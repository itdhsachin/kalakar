"""Validators for the accounts app.

This module contains a custom username validator for the accounts application.
"""

import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class ASCIIUsernameValidator(validators.RegexValidator):
    """Validator for usernames containing only ASCII characters.

    Inherits from:
        validators.RegexValidator

    Attributes:
        regex (str): The regular expression for validating the username.
        message (str): The error message to display for invalid usernames.
        flags (int): The flags to apply to the regular expression.
    """

    regex = r"^[a-zA-Z]+\/(...)\/(....)"
    message = _(
        "Enter a valid username. This value may contain only English letters, "
        "numbers, and @/./+/-/_ characters."
    )
    flags = re.ASCII
