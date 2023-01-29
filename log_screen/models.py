from datetime import date

from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Kullanıcı')
    customer_name = models.CharField(max_length=50, verbose_name='Müşteri Adı')
    customer_current = models.BooleanField(default=False, verbose_name='Mevcut Müşteri')
    customer_lead_date = models.DateField(verbose_name='Müşteri Ön Tarih')
    customer_update_date = models.DateField(auto_now=True, verbose_name='Güncellendi')

    def __str__(self):
        return self.customer_name

    class Meta:
        verbose_name = 'Müşteri'
        verbose_name_plural = 'Müşteriler'


class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Kullanıcı')
    project_customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Müşteri')
    project_start_date = models.DateField(verbose_name='Başlangıç Tarihi')
    project_finish_date = models.DateField(verbose_name='Bitiş Tarihi')
    project_business_unit = models.CharField(max_length=100, verbose_name='İş Ünitesi')
    project_type = models.CharField(max_length=100, verbose_name='Proje Tipi')

    def __str__(self):
        return f'{self.project_customer.customer_name} - {self.project_business_unit} - {self.project_type}'

    class Meta:
        verbose_name = 'Proje'
        verbose_name_plural = 'Projeler'


class Employee(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Kullanıcı')
    employee_first_name = models.CharField(max_length=50, verbose_name='Adı')
    employee_last_name = models.CharField(max_length=50, verbose_name='Soyadı')
    employee_birthdate = models.DateField(verbose_name='Doğum Tarihi')
    employee_start_date = models.DateField(verbose_name='Başlama Tarihi')
    employee_resignation_date = models.DateField(verbose_name='İstifa Tarihi', null=True, blank=True)
    employee_is_active = models.BooleanField(verbose_name='Aktif')
    employee_current_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Mevcut Proje')

    def __str__(self):
        return f'{self.employee_first_name} {self.employee_last_name} ({self.get_age()})'
    
    def get_age(self):
        today = date.today()
        age = today.year - self.employee_birthdate.year

        if today.month < self.employee_birthdate.month:
            age -= 1
        elif (today.month == self.employee_birthdate.month) and (self.employee_birthdate.day < today.day):
            age -= 1
        
        return age

    class Meta:
        verbose_name = 'Personel'
        verbose_name_plural = 'Personeller'


class EmployeeWork(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Kullanıcı')
    employeework_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Personel')
    employeework_current_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Mevcut Proje')
    employeework_daily_rate = models.FloatField(verbose_name='Günlük Değerlendirme')
    employeework_monthly_rate = models.FloatField(verbose_name='Aylık Değerlendirme')
    employeework_effort = models.FloatField(verbose_name='Çaba')
    employeework_effort_period = models.DateField(verbose_name='Çaba Dönemi')

    def __str__(self):
        return f'{self.employeework_employee} personalinin "{self.employeework_current_project}" işi'

    class Meta:
        verbose_name = 'Personel İşi'
        verbose_name_plural = 'Personel İşleri'
