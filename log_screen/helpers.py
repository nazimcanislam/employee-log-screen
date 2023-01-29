from datetime import datetime

from django.contrib import messages
from django.shortcuts import redirect

from .models import Customer, Project, Employee, EmployeeWork


def greeting(user):
    hour = datetime.now().hour
    text = ""

    name = user.first_name
    if user.last_name:
        name = f'{user.first_name} {user.last_name}'
    elif name == '' and user.last_name == '':
        name = user.username
    
    if user.is_superuser:
        name = f'<strong translate="no">{name} (admin)</strong>'
    else:
        name = f'<strong translate="no">{name}</strong>'

    if hour >= 5 and hour < 12:
        text = f'Günaydın {name} <span data-bs-toggle="tooltip" data-bs-title="Günaydın güneşi">☀️</span>'
    elif hour >= 12 and hour < 15:
        text = f'İyi Günler {name} <span data-bs-toggle="tooltip" data-bs-title="Havalı!">😎</span>'
    elif hour >= 15 and hour < 21:
        text = f'İyi Akşamlar {name} <span data-bs-toggle="tooltip" data-bs-title="Batan Güneş">🌅</span>'
    elif (hour >= 21 and hour < 24) or (hour >= 0 and hour < 5):
        text = f'İyi Geceler {name} <span data-bs-toggle="tooltip" data-bs-title="Uykulu">🥱</span>'
    else:
        text = f'İyi Zamansal Yolculuklar {name} <span data-bs-toggle="tooltip" data-bs-title="Şaşırmış">😶</span>'
    
    return text


def get_post_data_customer(request, model_name):
    customer_name = request.POST.get('customer-name-input')
    if customer_name == '':
        messages.add_message(request, messages.ERROR, 'Lütfen müşteri adını boş bırakmayınız!')
        return redirect('add_data', model_name=model_name)
    elif len(customer_name) < 3:
        messages.add_message(request, messages.ERROR, 'Lütfen en az 3 karakter uzunluğunda bir müşteri adı giriniz!')
        return redirect('add_data', model_name=model_name)
    else:
        customer_name = customer_name.strip().title()

    customer_lead_date = request.POST.get('customer-lead-date-input')
    if customer_lead_date == '':
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
    if not employee_current_project:
        messages.add_message(request, messages.ERROR, 'Lütfen personel için bir proje seçtiğinizden emin olunuz!')
        return redirect('add_data', model_name=model_name)
    
    try:
        employee_current_project = Project.objects.get(id=employee_current_project.split('-')[-1])
    except Project.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'Seçili proje verisi bulunamadı!')
        return redirect('add_data', model_name=model_name)

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
    if not employeework_daily_rate.isnumeric():
        messages.add_message(request, messages.ERROR, 'Lütfen günlük değerlendirme için bir sayı girdiğinizden emin olunuz!')
        return redirect('add_data', model_name=model_name)
    elif not (0 <= float(employeework_daily_rate) <= 100):
        messages.add_message(request, messages.ERROR, 'Lütfen günlük değerlendirme için 0 ile 100 arasında bir sayı girdiğinizden emin olunuz!')
        return redirect('add_data', model_name=model_name)
    employeework_daily_rate = float(employeework_daily_rate)

    employeework_monthly_rate = request.POST.get('employeework-monthly-rate-input')
    if not employeework_monthly_rate.isnumeric():
        messages.add_message(request, messages.ERROR, 'Lütfen aylık değerlendirme için bir sayı girdiğinizden emin olunuz!')
        return redirect('add_data', model_name=model_name)
    elif not (0 <= float(employeework_monthly_rate) <= 100):
        messages.add_message(request, messages.ERROR, 'Lütfen aylık değerlendirme için 0 ile 100 arasında bir sayı girdiğinizden emin olunuz!')
        return redirect('add_data', model_name=model_name)
    employeework_monthly_rate = float(employeework_monthly_rate)

    employeework_effort = request.POST.get('employeework-effort-input')
    if not employeework_effort.isnumeric():
        messages.add_message(request, messages.ERROR, 'Lütfen çaba değerlendirme için bir sayı girdiğinizden emin olunuz!')
        return redirect('add_data', model_name=model_name)
    elif not (0 <= float(employeework_effort) <= 100):
        messages.add_message(request, messages.ERROR, 'Lütfen çaba değerlendirme için 0 ile 100 arasında bir sayı girdiğinizden emin olunuz!')
        return redirect('add_data', model_name=model_name)
    employeework_effort = float(employeework_effort)

    employeework_effort_period = request.POST.get('employeework-effort-period-input')
    if employeework_effort_period == '':
        messages.add_message(request, messages.ERROR, 'Lütfen proje işinin çaba dönemi giriniz!')
        return redirect('add_data', model_name=model_name)
    else:
        employeework_effort_period = employeework_effort_period.strip()
    try:
        employeework_effort_period = datetime.strptime(employeework_effort_period, '%Y-%m-%d')
    except ValueError:
        messages.add_message(request, messages.ERROR, 'Lütfen proje işinin çaba dönemini doğru girdiğinizden emin olunuz! giriniz!')
        return redirect('add_data', model_name=model_name)

    return (employeework_employee, employeework_current_project, employeework_daily_rate, employeework_monthly_rate, employeework_effort, employeework_effort_period)
