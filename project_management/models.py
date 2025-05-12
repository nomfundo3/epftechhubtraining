from django.db import models
from system_management.models import User

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    company_reg_no = models.CharField(max_length=100)
    comapany_type = models.CharField(max_length=100)
    company_email = models.CharField(max_length=100)
    company_phone = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    company_address = models.CharField(max_length=300)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class UserCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE,related_name='user_companies')
     

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class DataPoint(models.Model):
    data_point_value = models.CharField(max_length=100) 
    date_recorded = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Form(models.Model):
    form_name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    project = models.OneToOneField(Project, on_delete=models.CASCADE)


class FormField(models.Model):
    field_name = models.CharField(max_length=100) 
    form = models.ForeignKey(Form, on_delete=models.CASCADE)


class UserProject(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

