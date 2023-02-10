from django.contrib import admin
from django.conf import settings

from .models import Customer, Project, Employee, EmployeeWork


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('author', 'customer_name', 'customer_current', 'customer_lead_date', 'customer_update_date')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('author', 'project_customer', 'project_start_date', 'project_finish_date', 'project_business_unit', 'project_type')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('author', 'employee_first_name', 'employee_last_name', 'employee_birthdate', 'employee_start_date', 'employee_resignation_date', 'employee_is_active', 'employee_current_project')


class EmployeeWorkAdmin(admin.ModelAdmin):
    list_display = ('author', 'employeework_employee', 'employeework_current_project', 'employeework_daily_rate', 'employeework_monthly_rate', 'employeework_effort', 'employeework_effort_period')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmployeeWork, EmployeeWorkAdmin)

admin.site.site_header = f'{settings.APP_LABEL} Kontrol Paneli'
admin.site.site_title = f'{settings.APP_LABEL} Kontrol Paneli'
