from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def get_app_version():
    return settings.APP_VERSION_NUMBER


@register.simple_tag
def get_app_label():
    return settings.APP_LABEL


@register.filter
def get_attribute(value, arg):
    arg = str(arg)
    if '.' in arg:
        arg = arg.split('.')[-1]

    return getattr(value, arg)


@register.filter
def to_str(value):
    return str(value)
