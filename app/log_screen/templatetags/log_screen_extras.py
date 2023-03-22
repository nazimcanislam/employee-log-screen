from django import template
from django.http import HttpRequest
from django.conf import settings

from ..models import Customer, Project, Employee, EmployeeWork


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


@register.simple_tag
def get_customers_count(request) -> int:
    return len(Customer.objects.filter(author=request.user))


@register.simple_tag
def get_projects_count(request) -> int:
    return len(Project.objects.filter(author=request.user))


@register.simple_tag
def get_employies_count(request) -> int:
    return len(Employee.objects.filter(author=request.user))


@register.simple_tag
def get_employeeworks_count(request) -> int:
    return len(EmployeeWork.objects.filter(author=request.user))


@register.simple_tag
def get_all_tables_count(request) -> int:
    return get_customers_count(request) + get_projects_count(request) + get_employies_count(request) + get_employeeworks_count(request)
