from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect

from .models import Customer, Project, Employee, EmployeeWork


def greeting(user: User) -> str:
    """A function that greets the user on the main page according to the current time.

    Args:
        user (User): Django user model to pick up user information.

    Returns:
        str: Returns a greeting message for user.
    """

    # Get the time and pass the time to the variable.
    hour: int = datetime.now().hour

    # Define a variable for the welcome text.
    text: str = ""

    # If user's last name is defined, use both first name and last name.
    # If there is only the first name, use it only.
    name: str = user.first_name
    if user.last_name:
        name = f'{user.first_name} {user.last_name}'
    elif name == '' and user.last_name == '':
        name = user.username
    
    # Specify if the user is a superuser.
    # In any case, prevent the user name from being translated by the browser.
    if user.is_superuser:
        name = f'<strong translate="no">{name} (admin)</strong>'
    else:
        name = f'<strong translate="no">{name}</strong>'

    # Set a greeting based on time.
    if hour >= 5 and hour < 12:
        text = f'<span>Günaydın</span> {name}'
    elif hour >= 12 and hour < 15:
        text = f'<span>İyi Günler</span> {name}'
    elif hour >= 15 and hour < 21:
        text = f'<span>İyi Akşamlar</span> {name}'
    elif (hour >= 21 and hour < 24) or (hour >= 0 and hour < 5):
        text = f'<span>İyi Geceler</span> {name}'
    else:
        text = f'<span>İyi Zamansal Yolculuklar</span> {name}'
    
    # Return the greeting value.
    return text


def get_post_data_customer(request, model_name):
    customer_name = request.POST.get('customer-name-input')
    if not customer_name:
        messages.add_message(request, messages.ERROR, 'Lütfen müşteri adını boş bırakmayınız!')
        return redirect('add_data', model_name=model_name)
    elif len(customer_name) < 3:
        messages.add_message(request, messages.ERROR, 'Lütfen en az 3 karakter uzunluğunda bir müşteri adı giriniz!')
        return redirect('add_data', model_name=model_name)
    else:
        customer_name = customer_name.strip().title()

    customer_lead_date = request.POST.get('customer-lead-date-input')
    if not customer_lead_date:
        messages.add_message(request, messages.ERROR, 'Lütfen müşterinin ön kayıt tarihini giriniz!')
        return redirect('add_data', model_name=model_name)
    else:
        customer_lead_date = customer_lead_date.strip()
    
    try:
        customer_lead_date = datetime.strptime(customer_lead_date, '%Y-%m-%d')
    except ValueError:
        messages.add_message(request, messages.ERROR, 'Lütfen müşterinin ön kayıt tarihini doğru girdiğinizden emin olunuz! giriniz!')
        return redirect('add_data', model_name=model_name)
    
    customer_current = bool(request.POST.get('customer-current-input'))

    return (customer_name, customer_current, customer_lead_date)


def get_post_data_project(request, model_name):
    project_customer = request.POST.get('project-customer-input')
    if not project_customer:
        messages.add_message(request, messages.ERROR, 'Lütfen proje için bir müşteri seçtiğinizden emin olunuz!')
        return redirect('add_data', model_name=model_name)
    try:
        project_customer = Customer.objects.get(id=project_customer.split('-')[-1])
    except Customer.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Seçili müşteri verisi bulunamadı!')
        return redirect('add_data', model_name=model_name)

    project_start_date = request.POST.get('project-start-date-input')
    if project_start_date:
        project_start_date = project_start_date.strip()
    else:
        messages.add_message(request, messages.ERROR, 'Lütfen projenin başlangıç tarihini giriniz!')
        return redirect('add_data', model_name=model_name)
    try:
        project_start_date = datetime.strptime(project_start_date, '%Y-%m-%d')
    except ValueError:
        messages.add_message(request, messages.ERROR, 'Lütfen projenin başlangıç tarihini doğru girdiğinizden emin olunuz! giriniz!')
        return redirect('add_data', model_name=model_name)
    
    project_finish_date = request.POST.get('project-finish-date-input')
    if project_finish_date:
        project_finish_date = project_finish_date.strip()
    else:
        messages.add_message(request, messages.ERROR, 'Lütfen projenin bitiş tarihini giriniz!')
        return redirect('add_data', model_name=model_name)
    
    try:
        project_finish_date = datetime.strptime(project_finish_date, '%Y-%m-%d')
    except ValueError:
        messages.add_message(request, messages.ERROR, 'Lütfen projenin bitiş tarihini doğru girdiğinizden emin olunuz! giriniz!')
        return redirect('add_data', model_name=model_name)
    project_business_unit = request.POST.get('project-business-unit-input')
    if project_business_unit:
        project_business_unit = project_business_unit.strip()
    else:
        messages.add_message(request, messages.ERROR, 'Lütfen proje ünitesini giriniz!')
        return redirect('add_data', model_name=model_name)
    
    project_type = request.POST.get('project-type-input')
    if project_type:
        project_type = project_type.strip()
    else:
        messages.add_message(request, messages.ERROR, 'Lütfen proje tipini giriniz!')
        return redirect('add_data', model_name=model_name)
    
    return (project_customer, project_start_date, project_finish_date, project_business_unit, project_type)


def get_post_data_employee(request, model_name):
    employee_first_name = request.POST.get('employee-first-name-input')
    if employee_first_name:
        employee_first_name = employee_first_name.strip().title()
    else:
        messages.add_message(request, messages.ERROR, 'Lütfen personel adını giriniz!')
        return redirect(f'/?model_name={model_name}')
    
    employee_last_name = request.POST.get('employee-last-name-input')
    if employee_last_name:
        employee_last_name = employee_last_name.strip().title()
    else:
        messages.add_message(request, messages.ERROR, 'Lütfen personel soyadını giriniz!')
        return redirect(f'/?model_name={model_name}')
    
    employee_birthdate = request.POST.get('employee-birthdate-input')
    if employee_birthdate:
        employee_birthdate = employee_birthdate.strip()
    else:
        messages.add_message(request, messages.ERROR, 'Lütfen personelin doğum tarihini giriniz!')
        return redirect('add_data', model_name=model_name)
    try:
        employee_birthdate = datetime.strptime(employee_birthdate, '%Y-%m-%d')
    except ValueError:
        messages.add_message(request, messages.ERROR, 'Lütfen personelin doğum tarihini doğru girdiğinizden emin olunuz! giriniz!')
        return redirect('add_data', model_name=model_name)
    
    employee_start_date = request.POST.get('employee-start-input')
    if employee_start_date:
        employee_start_date = employee_start_date.strip()
    else:
        messages.add_message(request, messages.ERROR, 'Lütfen personelin istifa tarihini giriniz!')
        return redirect('add_data', model_name=model_name)
    
    try:
        employee_start_date = datetime.strptime(employee_start_date, '%Y-%m-%d')
    except ValueError:
        messages.add_message(request, messages.ERROR, 'Lütfen personelin istifa tarihini doğru girdiğinizden emin olunuz! giriniz!')
        return redirect('add_data', model_name=model_name)
    
    employee_resignation_date = request.POST.get('employee-resignation-input')                 
    if employee_resignation_date:
        try:
            employee_resignation_date = datetime.strptime(employee_resignation_date, '%Y-%m-%d')
        except ValueError:
            messages.add_message(request, messages.ERROR, 'Lütfen personelin istifa tarihini doğru girdiğinizden emin olunuz! giriniz!')
            return redirect('add_data', model_name=model_name)
    else:
        employee_resignation_date = None
    
    employee_current_project = request.POST.get('employee-current-project-input')
    if employee_current_project:
        try:
            employee_current_project = Project.objects.get(id=employee_current_project.split('-')[-1])
        except Project.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Seçili proje verisi bulunamadı!')
            return redirect('add_data', model_name=model_name)
        except ValueError:
            employee_current_project = None

    employee_is_active = bool(request.POST.get('employee-is-active-input'))

    return (employee_first_name, employee_last_name, employee_birthdate, employee_start_date, employee_resignation_date, employee_current_project, employee_is_active)


def get_post_data_employeework(request, model_name):
    employeework_employee = request.POST.get('employeework-employee-input')
    if not employeework_employee:
        messages.add_message(request, messages.ERROR, 'Lütfen proje işi için bir personel seçtiğinizden emin olunuz!')
        return redirect('add_data', model_name=model_name)
    try:
        employeework_employee = Employee.objects.get(id=employeework_employee.split('-')[-1])
    except Employee.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Seçili personel verisi bulunamadı!')
        return redirect('add_data', model_name=model_name)
    
    employeework_current_project = request.POST.get('employeework-current-project-input')
    if not employeework_current_project:
        messages.add_message(request, messages.ERROR, 'Lütfen proje işi için bir proje seçtiğinizden emin olunuz!')
        return redirect('add_data', model_name=model_name)
    try:
        employeework_current_project = Project.objects.get(id=employeework_current_project.split('-')[-1])
    except Project.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Seçili proje verisi bulunamadı!')
        return redirect('add_data', model_name=model_name)
    
    employeework_daily_rate = request.POST.get('employeework-daily-rate-input')
    if employeework_daily_rate:
        if not employeework_daily_rate.isnumeric():
            messages.add_message(request, messages.ERROR, 'Lütfen günlük ücret için bir sayı girdiğinizden emin olunuz!')
            return redirect('add_data', model_name=model_name)
        elif int(employeework_daily_rate) < 0:
            messages.add_message(request, messages.ERROR, 'Lütfen günlük ücret için 0\'dan büyük bir sayı girdiğinizden emin olunuz!')
            return redirect('add_data', model_name=model_name)
        employeework_daily_rate = int(employeework_daily_rate)
    else:
        employeework_daily_rate = None

    employeework_monthly_rate = request.POST.get('employeework-monthly-rate-input')
    if employeework_monthly_rate:
        if not employeework_monthly_rate.isnumeric():
            messages.add_message(request, messages.ERROR, 'Lütfen aylık ücret için bir sayı girdiğinizden emin olunuz!')
            return redirect('add_data', model_name=model_name)
        elif int(employeework_monthly_rate) < 0:
            messages.add_message(request, messages.ERROR, 'Lütfen aylık ücret için 0\'dan büyük bir sayı girdiğinizden emin olunuz!')
            return redirect('add_data', model_name=model_name)
        employeework_monthly_rate = int(employeework_monthly_rate)
    else:
        employeework_monthly_rate = None

    employeework_effort = request.POST.get('employeework-effort-input')
    if employeework_effort:
        if not employeework_effort.isnumeric():
            messages.add_message(request, messages.ERROR, 'Lütfen efor ücret için bir sayı girdiğinizden emin olunuz!')
            return redirect('add_data', model_name=model_name)
        elif int(employeework_effort) < 0:
            messages.add_message(request, messages.ERROR, 'Lütfen efor ücret için 0\'dan büyük bir sayı girdiğinizden emin olunuz!')
            return redirect('add_data', model_name=model_name)
        employeework_effort = int(employeework_effort)
    else:
        employeework_effort = None

    employeework_effort_period = request.POST.get('employeework-effort-period-input')
    if employeework_effort_period == '':
        messages.add_message(request, messages.ERROR, 'Lütfen proje işinin efor dönemi giriniz!')
        return redirect('add_data', model_name=model_name)
    else:
        employeework_effort_period = employeework_effort_period.strip()
    try:
        employeework_effort_period = datetime.strptime(employeework_effort_period, '%Y-%m')
    except ValueError:
        messages.add_message(request, messages.ERROR, 'Lütfen proje işinin efor dönemini doğru girdiğinizden emin olunuz! giriniz!')
        return redirect('add_data', model_name=model_name)

    return (employeework_employee, employeework_current_project, employeework_daily_rate, employeework_monthly_rate, employeework_effort, employeework_effort_period)
