import django
import django.http

from django.apps import apps
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import logout as django_user_logout
from django.contrib.auth import login as django_user_login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from datetime import datetime

from . import helpers
from .apps import LogScreenConfig
from .models import Customer, Project, Employee, EmployeeWork
from .helpers import get_post_data_customer, get_post_data_project, get_post_data_employee, get_post_data_employeework


def index(request: django.http.HttpRequest):
    if not request.user.is_authenticated:
        return render(request, 'log_screen/introduction.html')
    
    greeting_message = helpers.greeting(request.user)

    models = list(apps.get_app_config(LogScreenConfig.name).get_models())
    models_names = [(model._meta.model_name, model._meta.verbose_name_plural.title()) for model in models]

    context = {
        'greeting_message': greeting_message,
        'models_names': models_names,
    }

    if request.GET.get('model_name') and request.user.is_authenticated:
        model_name = request.GET.get('model_name')

        for model in models:
            if model_name == model._meta.model_name:
                context['model_meta'] = model._meta
                
                model_objects_all = model.objects.filter(author=request.user)
                context['results'] = list(reversed(model_objects_all))

    return render(request, 'log_screen/index.html', context)


def login(request: django.http.HttpRequest):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get('username-input').strip()
        if username == '':
            messages.add_message(request, messages.ERROR, 'Lütfen E-Posta kısmını boş bırakmayınız!')
            return redirect('login')
        
        try:
            user = User.objects.get(username=username)
            if user:
                pass
        except User.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Hatalı kullanıcı adı veya parola!')
            return redirect('login')
        
        password = request.POST.get('password-input')
        if password == '':
            messages.add_message(request, messages.ERROR, 'Lütfen parola kısmını boş bırakmayınız!')
            return redirect('login')
        
        user = authenticate(username=username, password=password)
        if user:
            messages.add_message(request, messages.SUCCESS, f'Giriş yapma işlemi başarılı! Hoş geldiniz <strong>{user.first_name} {user.last_name}</strong> 😃')
            django_user_login(request, user)
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR, 'Hatalı kullanıcı adı veya parola!')
            return redirect('login')
    
    return render(request, 'log_screen/login.html')


def signup(request: django.http.HttpRequest):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        full_name = request.POST.get('fullname-input').strip()

        if full_name == '':
            messages.add_message(request, messages.ERROR, 'Lütfen ad soyad kısmını boş bırakmayınız!')
            return redirect('signup')
        elif len(full_name) < 3:
            messages.add_message(request, messages.ERROR, 'Lütfen en az 3 karakter uzunluğunda bir ad giriniz!')
            return redirect('signup')

        name_array = full_name.split(' ')
        name_array_length = len(name_array)
        
        if name_array_length == 1:
            first_name = name_array[0].title()
            last_name = None
        elif name_array_length == 2:
            first_name = name_array[0].title()
            last_name = name_array[1].title()
        else:
            last_name = name_array.pop()
            first_name = ' '.join(name_array).title()
        
        username = request.POST.get('username-input').strip().lower()
        if username == '':
            messages.add_message(request, messages.ERROR, 'Lütfen kullanıcı adı kısmını boş bırakmayınız!')
            return redirect('signup')
        elif len(username) < 5:
            messages.add_message(request, messages.ERROR, 'Lütfen en az 5 karakter uzunluğunda bir kullanıcı adı giriniz!')
            return redirect('signup')
        
        try:
            user = User.objects.get(username=username)
            if user:
                messages.add_message(request, messages.ERROR, 'Böyle bir kullanıcı adı zaten kullanımda!')
                return redirect('signup')
        except User.DoesNotExist:
            pass
        
        email = request.POST.get('email-input').strip()
        if email == '':
            messages.add_message(request, messages.ERROR, 'Lütfen E-Posta kısmını boş bırakmayınız!')
            return redirect('signup')
        
        try:
            user = User.objects.get(email=email)
            if user:
                messages.add_message(request, messages.ERROR, 'Böyle bir E-Posta adresi zaten kullanımda!')
                return redirect('signup')
        except User.DoesNotExist:
            pass

        password = request.POST.get('password-input')
        if password == '':
            messages.add_message(request, messages.ERROR, 'Lütfen parola kısmını boş bırakmayınız!')
            return redirect('signup')

        password_again = request.POST.get('password-again-input')
        if password_again == '':
            messages.add_message(request, messages.ERROR, 'Lütfen parola kısmını boş bırakmayınız!')
            return redirect('signup')
        
        if len(password) < 8 and len(password_again) < 8:
            messages.add_message(request, messages.ERROR, 'Lütfen en az 8 karakter uzunluğunda bir parola seçiniz!')
            return redirect('signup')
        
        if not any(list(map(lambda x: x.isupper(), password))):
            messages.add_message(request, messages.ERROR, 'Lütfen en az 1 büyük harf kullanınız!')
            return redirect('signup')

        if not any(list(map(lambda x: x.isnumeric(), password))):
            messages.add_message(request, messages.ERROR, 'Lütfen en az 1 sayı kullanınız!')
            return redirect('signup')
        
        if password != password_again:
            messages.add_message(request, messages.ERROR, 'Lütfen parolaların aynı olduğundan emin olunuz!')
            return redirect('signup')

        user = User()
        user.username = username
        user.first_name = first_name

        if last_name:
            user.last_name = last_name

        user.email = email
        user.set_password(password)

        try:
            user.save()
        except Exception:
            messages.add_message(request, messages.ERROR, 'Bilinmeyen bir hata meydana geldi! Lütfen daha sonra tekrar deneyiniz.')
            return redirect('signup')

        messages.add_message(request, messages.SUCCESS, 'Kayıt olma işlemi başarılı!')
        return redirect('login')

    return render(request, 'log_screen/signup.html')


def logout(request: django.http.HttpRequest):
    if request.user.is_authenticated:
        messages.add_message(request, messages.SUCCESS, 'Çıkış yapma işlemi başarılı! Görüşmek üzere.')
        django_user_logout(request)
        return redirect('login')
    
    return redirect('index')


def add_data_to_table(request: django.http.HttpRequest, model_name: str):
    if not request.user.is_authenticated:
        return redirect('index')

    try:
        model = apps.get_app_config(LogScreenConfig.name).get_model(model_name)
    except LookupError:
        messages.add_message(request, messages.ERROR, f'<strong translate="no">{model_name}</strong> adında bir tablo bulunamadı!')
        return redirect('index')

    context = {
        'model': model,
        'model_meta': model._meta,
        'include_form_name': f'log_screen/include/add_data_to_table_{model_name}.html',
        'adding': True
    }

    if request.method == 'POST':
        match model_name:
            case 'customer':
                customer_name, customer_current, customer_lead_date = get_post_data_customer(request, model_name)

                customer = Customer.objects.create(
                    author=request.user,
                    customer_name=customer_name,
                    customer_current=customer_current,
                    customer_lead_date=customer_lead_date
                )
                customer.save()

                messages.add_message(request, messages.SUCCESS, f'<strong>{model._meta.verbose_name_plural}</strong> tablosuna yeni kayıt ekleme başarılı!')
                return redirect(f'/?model_name={model_name}')
            case 'project':
                project_customer, project_start_date, project_finish_date, project_business_unit, project_type = get_post_data_project(request, model_name)
                
                project = Project.objects.create(
                    author=request.user,
                    project_customer=project_customer,
                    project_start_date=project_start_date,
                    project_finish_date=project_finish_date,
                    project_business_unit=project_business_unit,
                    project_type=project_type
                )
                project.save()

                messages.add_message(request, messages.SUCCESS, f'<strong>{model._meta.verbose_name_plural}</strong> tablosuna yeni kayıt ekleme başarılı!')
                return redirect(f'/?model_name={model_name}')
            case 'employee':
                employee_first_name, employee_last_name, employee_birthdate, employee_start_date, employee_resignation_date, employee_current_project, employee_is_active = get_post_data_employee(request, model_name)

                employee = Employee.objects.create(
                    author=request.user,
                    employee_first_name=employee_first_name,
                    employee_last_name=employee_last_name,
                    employee_birthdate=employee_birthdate,
                    employee_start_date=employee_start_date,
                    employee_resignation_date=employee_resignation_date,
                    employee_is_active=employee_is_active,
                    employee_current_project=employee_current_project
                )
                employee.save()

                messages.add_message(request, messages.SUCCESS, f'<strong>{model._meta.verbose_name_plural}</strong> tablosuna yeni kayıt ekleme başarılı!')
                return redirect(f'/?model_name={model_name}')
            case 'employeework':
                employeework_employee, employeework_current_project, employeework_daily_rate, employeework_monthly_rate, employeework_effort, employeework_effort_period = get_post_data_employeework(request, model_name)

                employeework = EmployeeWork.objects.create(
                    author=request.user,
                    employeework_employee=employeework_employee,
                    employeework_current_project=employeework_current_project,
                    employeework_daily_rate=employeework_daily_rate,
                    employeework_monthly_rate=employeework_monthly_rate,
                    employeework_effort=employeework_effort,
                    employeework_effort_period=employeework_effort_period
                )
                employeework.save()

                messages.add_message(request, messages.SUCCESS, f'<strong>{model._meta.verbose_name_plural}</strong> tablosuna yeni kayıt ekleme başarılı!')
                return redirect(f'/?model_name={model_name}')

    if model_name == 'project':
        context['customers'] = Customer.objects.filter(author=request.user)
        context['customer_meta'] = Customer._meta
    elif model_name == 'employee':
        context['projects'] = Project.objects.filter(author=request.user)
        context['project_meta'] = Project._meta
    elif model_name == 'employeework':
        context['employies'] = Employee.objects.filter(author=request.user)
        context['employee_meta'] = Employee._meta
        context['projects'] = Project.objects.filter(author=request.user)
        context['project_meta'] = Project._meta

    return render(request, 'log_screen/add_data_to_table.html', context)


def edit_data(request: django.http.HttpRequest, model_name: str, _id: int):
    if not request.user.is_authenticated:
        return redirect('index')

    try:
        model = apps.get_app_config(LogScreenConfig.name).get_model(model_name)
    except LookupError:
        messages.add_message(request, messages.ERROR, f'<strong translate="no">{model_name}</strong> adında bir tablo bulunamadı!')
        return redirect('index')
    
    context = {
        'model': model,
        'model_meta': model._meta,
        'include_form_name': f'log_screen/include/add_data_to_table_{model_name}.html',
        'editing': True,
        'data': model.objects.get(id=_id)
    }

    if request.method == 'POST':
        match model_name:
            case 'customer':
                customer_name, customer_current, customer_lead_date = get_post_data_customer(request, model_name)

                customer = Customer.objects.get(author=request.user, id=_id)
                customer.customer_name = customer_name
                customer.customer_current = customer_current
                # customer.customer_lead_date = customer_lead_date
                customer.customer_lead_date = "2020-01-01"
                customer.save()

                messages.add_message(request, messages.SUCCESS, f'{customer} değişikliği başarılı!')
                return redirect(f'/?model_name={model_name}')
            case 'project':
                project_customer, project_start_date, project_finish_date, project_business_unit, project_type = get_post_data_project(request, model_name)
                
                project = Project.objects.get(author=request.user, id=_id)
                project.project_customer = project_customer
                project.project_start_date = project_start_date
                project.project_finish_date = project_finish_date
                project.project_business_unit = project_business_unit
                project.project_type = project_type
                project.save()

                messages.add_message(request, messages.SUCCESS, f'{project} değişikliği başarılı!')
                return redirect(f'/?model_name={model_name}')
            case 'employee':
                employee_first_name, employee_last_name, employee_birthdate, employee_start_date, employee_resignation_date, employee_current_project, employee_is_active = get_post_data_employee(request, model_name)

                employee = Employee.objects.get(author=request.user, id=_id)
                employee.employee_first_name = employee_first_name
                employee.employee_last_name = employee_last_name
                employee.employee_birthdate = employee_birthdate
                employee.employee_start_date = employee_start_date
                employee.employee_resignation_date = employee_resignation_date
                employee.employee_current_project = employee_current_project
                employee.employee_is_active = employee_is_active
                employee.save()

                messages.add_message(request, messages.SUCCESS, f'{employee} değişikliği başarılı!')
                return redirect(f'/?model_name={model_name}')
            case 'employeework':
                employeework_employee, employeework_current_project, employeework_daily_rate, employeework_monthly_rate, employeework_effort, employeework_effort_period = get_post_data_employeework(request, model_name)

                employeework = EmployeeWork.objects.get(author=request.user, id=_id)
                employeework.employeework_employee = employeework_employee
                employeework.employeework_current_project = employeework_current_project
                employeework.employeework_daily_rate = employeework_daily_rate
                employeework.employeework_monthly_rate = employeework_monthly_rate
                employeework.employeework_effort = employeework_effort
                employeework.employeework_effort_period = employeework_effort_period
                employeework.save()

                messages.add_message(request, messages.SUCCESS, f'{employeework_effort_period} değişikliği başarılı!')
                return redirect(f'/?model_name={model_name}')

    if model_name == 'project':
        context['customers'] = Customer.objects.filter(author=request.user)
        context['customer_meta'] = Customer._meta
    elif model_name == 'employee':
        context['projects'] = Project.objects.filter(author=request.user)
        context['project_meta'] = Project._meta
    elif model_name == 'employeework':
        context['employies'] = Employee.objects.filter(author=request.user)
        context['employee_meta'] = Employee._meta
        context['projects'] = Project.objects.filter(author=request.user)
        context['project_meta'] = Project._meta

    return render(request, 'log_screen/add_data_to_table.html', context)


def delete_data(request: django.http.HttpRequest, model_name: str, _id: int):
    if not request.user.is_authenticated:
        return redirect('index')
    
    match model_name:
        case 'customer':
            Customer.objects.get(author=request.user, id=_id).delete()
        case 'project':
            Project.objects.get(author=request.user, id=_id).delete()
        case 'employee':
            Employee.objects.get(author=request.user, id=_id).delete()
        case 'employeework':
            EmployeeWork.objects.get(author=request.user, id=_id).delete()
    
    messages.add_message(request, messages.SUCCESS, 'Veri silindi.')
    return redirect(f'/?model_name={model_name}')
