import datetime
from django.db import models
from django.utils  import timezone
from django.contrib.auth.models import User
# Create your models here.

class Department(models.Model):
    name=models.CharField(max_length=30)
    description=models.CharField(max_length=255)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number=models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    department=models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    hire_date=models.DateField(blank=True, null=True)
    # Following are the settings of warehouse staff labelling item using customized bar code
    item_start=models.IntegerField(blank=True, null=True)
    item_end=models.IntegerField(blank=True, null=True)
    item_version=models.IntegerField(blank=True, null=True)
    last_issued_number=models.IntegerField(blank=True, null=True)
    last_modify_number_date=models.DateField(blank=True, null=True)
