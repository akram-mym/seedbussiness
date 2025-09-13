from datetime import date
import os
import random
from django.db import models
from django.core.exceptions import ValidationError


class Company(models.Model):
    com_id = models.CharField(max_length=20,primary_key=True)
    company_name = models.CharField(max_length=100, unique=True)
    company_email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)  # 👈 Add this
    def __str__(self):
        return self.company_name   # 👈 This makes the dropdown readable


class DealingYear(models.Model):
    STATUS_CHOICES = [
        ('Stop', 'Stop'),
        ('On', 'On'),
        ('Abuse', 'Abuse'),
    ]
    
    dy_session = models.CharField(max_length=20, primary_key=True)  # অর্থবছর বা সেশন
    busy_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='On')
    com_id = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.dy_session}"

    class Meta:
        db_table = 'dealing_year'  # বিদ্যমান টেবিলের সাথে মিল


   # ✅ Step 1: ছবি আপলোড পাথ নির্ধারণ ফাংশন (save এর বাইরে রাখতে হবে)
def employee_picture_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    emp_id = instance.EmpId or 'temp'
    filename = f"{emp_id}.{ext}"
    return os.path.join('img/employee_pictures/', filename)


class Employee(models.Model):
    EmpId = models.CharField(max_length=10, primary_key=True)
    EmpName = models.CharField(max_length=100)
    EmpDesig = models.CharField(max_length=100)
    EmpMobile = models.CharField(max_length=15, unique=True)
    EmpEmail = models.EmailField(max_length=50, unique=True)
    EmpBirthDate = models.DateField()
    EmpJoininghDate = models.DateField()    
    EmpPicture = models.ImageField(upload_to=employee_picture_upload_path, blank=True, null=True)
    EmpStatus = models.CharField(max_length=10, default='ON')
    EmpComId = models.ForeignKey(Company, on_delete=models.CASCADE)

    def clean(self):
        if self.EmpBirthDate and self.EmpBirthDate > date.today():
            raise ValidationError("জন্মতারিখ আজকের পরে হতে পারে না।")

    def save(self, *args, **kwargs):
        # ✅ Step 2: ইউনিক EmpId তৈরি
        if not self.EmpId:
            while True:
                number = random.randint(1000, 9999)
                emp_id = f"E{number}"
                if not Employee.objects.filter(EmpId=emp_id).exists():
                    self.EmpId = emp_id
                    break

        # ✅ Step 3: সেভ করুন
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.EmpId} - {self.EmpName}"
            

class Catagory(models.Model):
    catagoryid = models.AutoField(primary_key=True) 
    catagoryName =models.CharField(max_length=100,unique=True)  
    catagory_short =models.CharField(max_length=20,unique=True)  
    ComId = models.ForeignKey(Company, on_delete=models.CASCADE)  

    def __str__(self):
        return F"{self.catagory_short}-{self.catagoryName}"    