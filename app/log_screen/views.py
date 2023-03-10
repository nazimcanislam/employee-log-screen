import csv
import json
import datetime

from django.http import HttpRequest
from django.apps import apps
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import logout as django_user_logout
from django.contrib.auth import login as django_user_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from . import helpers
from .apps import LogScreenConfig
from .models import Customer, Project, Employee, EmployeeWork
from .helpers import get_post_data_customer, get_post_data_project, get_post_data_employee, get_post_data_employeework


def index(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return render(request, 'log_screen/introduction.html')
    
    greeting_message = helpers.greeting(request.user)

    context = {
        'greeting_message': greeting_message,
    }

    return render(request, 'log_screen/index.html', context)


@login_required
def index_show_table(request: HttpRequest, table_name: str) -> HttpResponse:
    greeting_message = helpers.greeting(request.user)

    context = {
        'greeting_message': greeting_message,
        'table_name': table_name
    }

    match table_name:
        case 'customer':
            context['table_verbose_name'] = Customer._meta.verbose_name
            context['table_verbose_name_plural'] = Customer._meta.verbose_name_plural
            context['results'] = Customer.objects.filter(author=request.user)
        case 'project':
            context['table_verbose_name'] = Project._meta.verbose_name
            context['table_verbose_name_plural'] = Project._meta.verbose_name_plural
            context['results'] = Project.objects.filter(author=request.user)
        case 'employee':
            context['table_verbose_name'] = Employee._meta.verbose_name
            context['table_verbose_name_plural'] = Employee._meta.verbose_name_plural
            context['results'] = Employee.objects.filter(author=request.user)
        case 'employeework':
            context['table_verbose_name'] = EmployeeWork._meta.verbose_name
            context['table_verbose_name_plural'] = EmployeeWork._meta.verbose_name_plural
            context['results'] = EmployeeWork.objects.filter(author=request.user)
        case _:
            return redirect('index')
    
    context['search_results'] = context['results']
    context['table_include'] = f'log_screen/include/tables/data/{table_name}.html'
    context['subtitle'] = context['table_verbose_name_plural']

    if request.GET.get('search-input'):
        search: str = request.GET.get('search-input')
        match table_name:
            case 'customer':
                customers = Customer.objects.filter(author=request.user)
                results = [customer for customer in customers if search.lower() in str(customer).lower()]
                context['results'] = results
            case 'project':
                projects = Project.objects.filter(author=request.user)
                results = [project for project in projects if search.lower() in str(project).lower()]
                context['results'] = results
            case 'employee':
                employies = Employee.objects.filter(author=request.user)
                results = [employee for employee in employies if search.lower() in str(employee).lower()]
                context['results'] = results
            case 'employeework':
                employeeworks = EmployeeWork.objects.filter(author=request.user)
                results = [employeework for employeework in employeeworks if search.lower() in str(employeework).lower()]
                context['results'] = results
            case _:
                return redirect('index')

        context['search'] = search

    return render(request, 'log_screen/index.html', context)


@login_required
def index_show_report(request: HttpRequest, report_name: str) -> HttpResponse:
    greeting_message = helpers.greeting(request.user)

    context = {
        'greeting_message': greeting_message,
        'model_name': report_name
    }

    match report_name:
        case 'employeework':
            context['report_name'] = 'Personeller ????leri Raporlar??'
            context['report_table_include'] = f'log_screen/include/tables/report/{report_name}.html'
            context['employeeworks'] = EmployeeWork.objects.filter(author=request.user)
        case 'customer':
            customers = Customer.objects.filter(author=request.user)
            context['report_name'] = 'M????teri Raporlar??'
            context['report_table_include'] = f'log_screen/include/tables/report/{report_name}.html'
            context['customers'] = customers

            employee_works = EmployeeWork.objects.filter(author=request.user)
            for employee_work in employee_works:
                for customer in customers:
                    if customer.id == employee_work.employeework_current_project.project_customer.id:
                        try:
                            customer.total_effort += employee_work.calculate_effort()
                        except AttributeError:
                            customer.total_effort = employee_work.calculate_effort()
        case _:
            return redirect('index')
    
    context['subtitle'] = context['report_name']
    
    return render(request, 'log_screen/index.html', context)


@login_required
def reqort_output(request: HttpRequest, report_name: str, output_type: str) -> HttpResponse:
    now = datetime.datetime.now()
    now_string = f'{now.year}-{now.month}-{now.day}'

    match report_name:
        case 'employeework':
            employee_works = EmployeeWork.objects.filter(author=request.user)
            if employee_works:
                match output_type:
                    case 'csv':
                        resposne = HttpResponse(
                            content_type='text/csv; charset=utf-8',
                            headers={'Content-Disposition': f'attachment; filename="employee_works_report-{now_string}.csv"'}
                        )

                        writer = csv.writer(resposne)
                        writer.writerow(['Tarih', 'Personel', 'M????teri', 'Efor', '??cret (G??nl??k) (TRY)', '??cret (Ayl??k) (TRY)', 'Toplam'])

                        for employee_work in employee_works:
                            writer.writerow(
                                [
                                    str(employee_work.employeework_effort_period).replace('-', '/'),
                                    str(employee_work.employeework_employee),
                                    str(employee_work.employeework_current_project.project_customer),
                                    employee_work.employeework_effort,
                                    str(employee_work.employeework_daily_rate).replace('.', ',') if employee_work.employeework_daily_rate else '0,0',
                                    str(employee_work.employeework_monthly_rate).replace('.', ',') if employee_work.employeework_monthly_rate else '0,0',
                                    str(employee_work.calculate_effort()).replace('.', ','),
                                ]
                            )
                        
                        return resposne
                    case 'json':
                        json_object = []

                        for employee_work in employee_works:
                            json_object.append(
                                {
                                    'effort_period': str(employee_work.employeework_effort_period).replace('-', '/'),
                                    'employee': str(employee_work.employeework_employee),
                                    'customer': str(employee_work.employeework_current_project.project_customer),
                                    'effort': int(employee_work.employeework_effort),
                                    'daily_rate': float('{:.2f}'.format(employee_work.employeework_daily_rate) if employee_work.employeework_daily_rate else 0),
                                    'monthly_rate': float('{:.2f}'.format(employee_work.employeework_monthly_rate) if employee_work.employeework_monthly_rate else 0),
                                    'total_rate': float('{:.2f}'.format(employee_work.calculate_effort())),
                                }
                            )

                        resposne = HttpResponse(
                            content=json.dumps(json_object, indent=2, ensure_ascii=False),
                            content_type='application/json; charset=utf-8',
                            headers={'Content-Disposition': f'attachment; filename="employee_works_report-{now_string}.json"'}
                        )

                        return resposne
                    case _:
                        return redirect('index')
        case 'customer':
            customers = Customer.objects.filter(author=request.user)
            employee_works = EmployeeWork.objects.filter(author=request.user)
            if customers and employee_works:
                match output_type:
                    case 'csv':
                        resposne = HttpResponse(
                            content_type='text/csv; charset=utf-8',
                            headers={'Content-Disposition': f'attachment; filename="customers_report-{now_string}.csv"'}
                        )

                        writer = csv.writer(resposne)
                        writer.writerow(['M????teri ??n Tarih', 'M????teri', 'Toplam'])

                        for customer in customers:
                            total_effort = 0
                            for employee_work in employee_works:
                                if employee_work.employeework_current_project.project_customer.id == customer.id:
                                    total_effort += employee_work.calculate_effort()

                            writer.writerow(
                                [
                                    str(customer.customer_lead_date).replace('-', '/'),
                                    str(customer),
                                    float('{:.2f}'.format(total_effort)),
                                ]
                            )
                        
                        return resposne
                    case 'json':
                        json_object = []

                        for customer in customers:
                            total_effort = 0
                            for employee_work in employee_works:
                                if employee_work.employeework_current_project.project_customer.id == customer.id:
                                    total_effort += employee_work.calculate_effort()
    
                            json_object.append(
                                {
                                    'customer_lead_date': str(customer.customer_lead_date).replace('-', '/'),
                                    'customer': str(customer),
                                    'total_rate': float('{:.2f}'.format(total_effort)),
                                }
                            )

                        resposne = HttpResponse(
                            content=json.dumps(json_object, indent=2, ensure_ascii=False),
                            content_type='application/json; charset=utf-8',
                            headers={'Content-Disposition': f'attachment; filename="customers_report-{now_string}.json"'}
                        )

                        return resposne
                    case _:
                        return redirect('index')
        case _:
            return redirect('index')
    
    return redirect('index')


def login(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get('username-input').strip()
        if not username:
            messages.add_message(request, messages.ERROR, 'L??tfen E-Posta k??sm??n?? bo?? b??rakmay??n??z!')
            return redirect('login')
        
        try:
            user = User.objects.get(username=username)
            if user:
                pass
        except User.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Hatal?? kullan??c?? ad?? veya parola!')
            return redirect('login')
        
        password = request.POST.get('password-input')
        if not password:
            messages.add_message(request, messages.ERROR, 'L??tfen parola k??sm??n?? bo?? b??rakmay??n??z!')
            return redirect('login')
        
        user = authenticate(username=username, password=password)
        if user:
            messages.add_message(request, messages.SUCCESS, f'<span>Giri?? yapma i??lemi ba??ar??l??! Ho?? geldiniz </span> <strong translate="no">{user.first_name} {user.last_name}</strong> ????')
            django_user_login(request, user)
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR, 'Hatal?? kullan??c?? ad?? veya parola!')
            return redirect('login')
    
    return render(request, 'log_screen/login.html')


def signup(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        full_name = request.POST.get('fullname-input').strip()

        if not full_name:
            messages.add_message(request, messages.ERROR, 'L??tfen ad soyad k??sm??n?? bo?? b??rakmay??n??z!')
            return redirect('signup')
        elif len(full_name) < 3:
            messages.add_message(request, messages.ERROR, 'L??tfen en az 3 karakter uzunlu??unda bir ad giriniz!')
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
        if not username:
            messages.add_message(request, messages.ERROR, 'L??tfen kullan??c?? ad?? k??sm??n?? bo?? b??rakmay??n??z!')
            return redirect('signup')
        elif len(username) < 5:
            messages.add_message(request, messages.ERROR, 'L??tfen en az 5 karakter uzunlu??unda bir kullan??c?? ad?? giriniz!')
            return redirect('signup')
        
        try:
            user = User.objects.get(username=username)
            if user:
                messages.add_message(request, messages.ERROR, 'B??yle bir kullan??c?? ad?? zaten kullan??mda!')
                return redirect('signup')
        except User.DoesNotExist:
            pass
        
        email = request.POST.get('email-input').strip()
        if not email:
            messages.add_message(request, messages.ERROR, 'L??tfen E-Posta k??sm??n?? bo?? b??rakmay??n??z!')
            return redirect('signup')
        
        try:
            user = User.objects.get(email=email)
            if user:
                messages.add_message(request, messages.ERROR, 'B??yle bir E-Posta adresi zaten kullan??mda!')
                return redirect('signup')
        except User.DoesNotExist:
            pass

        password = request.POST.get('password-input')
        if password == '':
            messages.add_message(request, messages.ERROR, 'L??tfen parola k??sm??n?? bo?? b??rakmay??n??z!')
            return redirect('signup')

        password_again = request.POST.get('password-again-input')
        if password_again == '':
            messages.add_message(request, messages.ERROR, 'L??tfen parola k??sm??n?? bo?? b??rakmay??n??z!')
            return redirect('signup')
        
        if len(password) < 8 and len(password_again) < 8:
            messages.add_message(request, messages.ERROR, 'L??tfen en az 8 karakter uzunlu??unda bir parola se??iniz!')
            return redirect('signup')
        
        if not any(list(map(lambda x: x.isupper(), password))):
            messages.add_message(request, messages.ERROR, 'L??tfen en az 1 b??y??k harf kullan??n??z!')
            return redirect('signup')

        if not any(list(map(lambda x: x.isnumeric(), password))):
            messages.add_message(request, messages.ERROR, 'L??tfen en az 1 say?? kullan??n??z!')
            return redirect('signup')
        
        if password != password_again:
            messages.add_message(request, messages.ERROR, 'L??tfen parolalar??n ayn?? oldu??undan emin olunuz!')
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
            messages.add_message(request, messages.ERROR, 'Bilinmeyen bir hata meydana geldi! L??tfen daha sonra tekrar deneyiniz.')
            return redirect('signup')

        messages.add_message(request, messages.SUCCESS, 'Kay??t olma i??lemi ba??ar??l??!')
        return redirect('login')

    return render(request, 'log_screen/signup.html')


def logout(request: HttpRequest) -> HttpResponseRedirect:
    """User sign out view

    Args:
        request (HttpRequest): Request sent

    Returns:
        HttpResponseRedirect: Redirected page after model deletion
    """

    # If the user is logged in, log out.
    # Record successful logout and redirect to login page.
    if request.user.is_authenticated:
        messages.add_message(request, messages.SUCCESS, '????k???? yapma i??lemi ba??ar??l??! G??r????mek ??zere.')
        django_user_logout(request)
        return redirect('login')
    
    # If there is no user login, redirect to the home page.
    return redirect('index')


@login_required
def add_data_to_table(request: HttpRequest, model_name: str) -> HttpResponse:
    try:
        model = apps.get_app_config(LogScreenConfig.name).get_model(model_name)
    except LookupError:
        messages.add_message(request, messages.ERROR, f'<strong translate="no">{model_name}</strong> ad??nda bir tablo bulunamad??!')
        return redirect('index')

    context = {
        'model': model,
        'model_meta': model._meta,
        'include_form_name': f'log_screen/include/forms/add/{model_name}.html',
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
                messages.add_message(request, messages.SUCCESS, f'<strong>{model._meta.verbose_name_plural}</strong> tablosuna yeni kay??t ekleme ba??ar??l??!')
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
                messages.add_message(request, messages.SUCCESS, f'<strong>{model._meta.verbose_name_plural}</strong> tablosuna yeni kay??t ekleme ba??ar??l??!')
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
                messages.add_message(request, messages.SUCCESS, f'<strong>{model._meta.verbose_name_plural}</strong> tablosuna yeni kay??t ekleme ba??ar??l??!')
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
                messages.add_message(request, messages.SUCCESS, f'<strong>{model._meta.verbose_name_plural}</strong> tablosuna yeni kay??t ekleme ba??ar??l??!')

        return redirect('index_show_table', table_name=model_name)

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

    return render(request, 'log_screen/add_or_edit_data.html', context)


@login_required
def edit_data(request: HttpRequest, model_name: str, _id: int) -> HttpResponse:
    try:
        model = apps.get_app_config(LogScreenConfig.name).get_model(model_name)
    except LookupError:
        messages.add_message(request, messages.ERROR, f'<strong translate="no">{model_name}</strong> ad??nda bir tablo bulunamad??!')
        return redirect('index')
    
    context = {
        'model': model,
        'model_meta': model._meta,
        'include_form_name': f'log_screen/include/forms/add/{model_name}.html',
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
                customer.customer_lead_date = customer_lead_date
                customer.save()
                messages.add_message(request, messages.SUCCESS, f'{customer} de??i??ikli??i ba??ar??l??!')
            case 'project':
                project_customer, project_start_date, project_finish_date, project_business_unit, project_type = get_post_data_project(request, model_name)
                
                project = Project.objects.get(author=request.user, id=_id)
                project.project_customer = project_customer
                project.project_start_date = project_start_date
                project.project_finish_date = project_finish_date
                project.project_business_unit = project_business_unit
                project.project_type = project_type
                project.save()
                messages.add_message(request, messages.SUCCESS, f'{project} de??i??ikli??i ba??ar??l??!')
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
                messages.add_message(request, messages.SUCCESS, f'{employee} de??i??ikli??i ba??ar??l??!')
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
                messages.add_message(request, messages.SUCCESS, f'{employeework} de??i??ikli??i ba??ar??l??!')
        
        return redirect('index_show_table', table_name=model_name)

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

    return render(request, 'log_screen/add_or_edit_data.html', context)


@login_required
def delete_data_view(request: HttpRequest, model_name: str, _id: int) -> HttpResponseRedirect:
    """A view that deletes data from models.

    Args:
        request (HttpRequest): Request sent
        model_name (str): Model type to be deleted
        _id (int): Model id to be deleted

    Returns:
        HttpResponseRedirect: Redirected page after model deletion
    """

    # To delete a model, check the requested model name. If there is a match, try deleting it.
    # If there is no match, return it to the tables.
    # In case of any error, create a message and redirect it to the homepage.
    try:
        match model_name:
            case 'customer':
                Customer.objects.get(author=request.user, id=_id).delete()
            case 'project':
                Project.objects.get(author=request.user, id=_id).delete()
            case 'employee':
                Employee.objects.get(author=request.user, id=_id).delete()
            case 'employeework':
                EmployeeWork.objects.get(author=request.user, id=_id).delete()
            case _:
                return redirect('index_show_table', table_name=model_name)
    except Exception:
        messages.add_message(request, messages.WARNING, 'Bilinmeyen bir sorun olu??tu! Neyse ki g??venli bir yere d??nd??k.')
        return redirect('index_show_table', table_name=model_name)
    
    # If there is no problem, create message and redirect back to tables.
    messages.add_message(request, messages.SUCCESS, 'Veri silindi.')
    return redirect('index_show_table', table_name=model_name)
