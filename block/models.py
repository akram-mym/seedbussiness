import os
from django.db import models

# from ProjectAdmin.models import Catagory
from ProjectAdmin.models import Catagory
from account.models import SubHead
from django.contrib.auth.models import User

# Create your models here.




class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    block_id = models.CharField(max_length=20)
    sub_code = models.ForeignKey(SubHead, on_delete=models.CASCADE)
    byear = models.CharField(max_length=20)
    com_id = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('block_id', 'sub_code', 'byear', 'com_id', 'user')

    def __str__(self):
        return f"Budget {self.byear} ({self.sub_code}) - {self.user.username}"    

def person_picture_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    person_id = instance.person_id or 'temp'
    filename = f"{person_id}.{ext}"
    return os.path.join('img/person_pictures/', filename)

def person_nid_picture_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    person_id = instance.person_id or 'temp'
    filename = f"{person_id}.{ext}"
    return os.path.join('img/person_nid_pictures/', filename)

class Person(models.Model):         
     user        = models.ForeignKey(User, on_delete=models.CASCADE)
     block_id    = models.CharField(max_length=20) 
     catagory_short = models.ForeignKey(Catagory,on_delete=models.CASCADE)   
     person_id   = models.CharField(max_length=30)
     nid_no      = models.CharField(max_length=30)
     first_name  = models.CharField(max_length=20)
     last_name   = models.CharField(max_length=30)
     father_name = models.CharField(max_length=50)
     mobile_no   = models.CharField(max_length=14)
     address     = models.TextField()
     person_picture = models.ImageField(upload_to=person_picture_upload_path, blank=True, null=True)
     person_nid_picture = models.ImageField(upload_to=person_nid_picture_upload_path, blank=True, null=True)
     com_id = models.CharField(max_length=20)
     created_at = models.DateTimeField(auto_now_add=True)
    

     class Meta:
        unique_together = ('catagory_short', 'mobile_no')
    
     def __str__(self):
        return f"{self.person_id} {self.catagory_short}"  # dropdown এ নাম দেখাবে



class LandMeasure(models.Model):
    edate = models.DateField()  # Entry/created date
    b_id = models.CharField(max_length=20)  # Building/Block ID
    plot_no = models.CharField(max_length=100)  # Plot number (string, can adjust length)
    llid = models.ForeignKey(Person, on_delete=models.CASCADE)  # Land/Location ID
    length1 = models.DecimalField(max_digits=10, decimal_places=2)  # Length side 1
    length2 = models.DecimalField(max_digits=10, decimal_places=2)  # Length side 2
    width1 = models.DecimalField(max_digits=10, decimal_places=2)   # Width side 1
    width2 = models.DecimalField(max_digits=10, decimal_places=2)   # Width side 2
    deci = models.DecimalField(max_digits=10, decimal_places=2)  # Decimal measurement
    paid = models.BooleanField(default=False)  # Payment status
    state = models.CharField(max_length=100)  # State/Status
    com_id = models.CharField(max_length=20)  # Company ID

    def __str__(self):
        return f"Plot {self.plot_no} - {self.state}"        
    

class SeedTransport(models.Model):
    sending_date = models.DateField()    
    b_id = models.CharField(max_length=20)
    chalan_no = models.CharField(max_length=20)
    seed_sent = models.IntegerField()
    seed_received = models.IntegerField(default=0)
    empty_bags = models.IntegerField(default=0)
    variety_name = models.CharField(max_length=50)
    driver_name = models.CharField(max_length=50)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField(null=True, blank=True)
    duration = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # in hours, for example
    day = models.CharField(max_length=20)
    com_id = models.CharField(max_length=20)



