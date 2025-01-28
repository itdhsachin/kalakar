"""Template tags."""

from django import template

register = template.Library()


@register.filter
def model_name(obj):
    """Model method."""
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
