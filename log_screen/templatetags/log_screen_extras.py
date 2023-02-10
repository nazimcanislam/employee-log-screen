from django import template
from django.conf import settings


# Create Django template library for making custom template tools for Log Screen app.
register = template.Library()


@register.simple_tag
def get_app_version() -> str:
    """Retruns application version from global Django settings file.

    Returns:
        str: Application version
    """

    # Return application version from settings.
    return settings.APP_VERSION_NUMBER


@register.simple_tag
def get_app_label() -> str:
    """Retruns application name from global Django settings file.

    Returns:
        str: Application name
    """

    # Return application name from settings.
    return settings.APP_LABEL
