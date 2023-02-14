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
        """Calculate and return the age of the employee.

        Returns:
            int: Employee age
        """

        # Take today's date and assign it to variable.
        today = date.today()

        # Subtract the employee year from the present year.
        age = today.year - self.employee_birthdate.year

        # Check the birth month and birthday of the employee and reduce the age by 1 accordingly.
        if today.month < self.employee_birthdate.month:
            age -= 1
        elif (today.month == self.employee_birthdate.month) and (self.employee_birthdate.day < today.day):
            age -= 1

        # Return the employee age.
        return age

    class Meta:
        verbose_name = 'Personel'
        verbose_name_plural = 'Personeller'


class EmployeeWork(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Kullanıcı')
    employeework_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Personel')
    employeework_current_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Mevcut Proje')
    employeework_daily_rate = models.FloatField(verbose_name='Günlük Ücret', null=True, blank=True)
    employeework_monthly_rate = models.FloatField(verbose_name='Aylık Ücret', null=True, blank=True)
    employeework_effort = models.IntegerField(verbose_name='Efor', null=True, blank=True)
    employeework_effort_period = models.DateField(verbose_name='Efor Dönemi')

    def __str__(self):
        return f'{self.employeework_employee} personalinin "{self.employeework_current_project}" işi'
    
    def readable_effort(self) -> str:
        """Calculates effort days and returns human readable days count.

        Returns:
            str: Readable days count
        """

        # As long as the number of effort days is greater than or equal to 30,
        # decrease the number of days of effort by 30 and increase the month variable.
        days = self.employeework_effort
        months = 0
        while days >= 30:
            days -= 30
            months += 1
        
        # If month and day are greater than 0, use both.
        # Use month or day whichever is greater than 0.
        text = ''
        if months > 0 and days > 0:
            text = f'{months} ay {days} gün'
        elif months > 0:
            text = f'{months} ay'
        elif days > 0:
            text = f'{days} gün'
        
        # Return the result readable text.
        return text

    def calculate_effort(self) -> float:
        """It multiplies the employee's diary with effort and their salary with effort and returns them.

        Result = (Daily Rate * Effort) + (Monthly Rate * Effort)

        Returns:
            float: Calculated total fee
        """

        # If you have both daily and monthly, consider both.
        # If there is only daily, only take the daily calculation.
        # If there is only month, only take the monthly calculation.
        if self.employeework_daily_rate and self.employeework_monthly_rate:
            return (self.employeework_daily_rate * self.employeework_effort) + (self.employeework_monthly_rate * self.employeework_effort)
        elif self.employeework_daily_rate:
            return self.employeework_daily_rate * self.employeework_effort
        elif self.employeework_monthly_rate:
            return self.employeework_monthly_rate * self.employeework_effort

        # Return zero if no fee is specified.
        return 0.0

    class Meta:
        verbose_name = 'Personel İşi'
        verbose_name_plural = 'Personeller İşleri'
