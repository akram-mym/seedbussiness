from django.db import models
from django.utils.timezone import localtime
# Create your models here.
from django.db import models

from ProjectAdmin.models import Company, DealingYear, Employee


    
DIVISION_CHOICES = [
        ('AC', 'Account'),
        ('SP', 'Seed Production'),
        ('SM', 'Seed Marketing'),
    ]


def current_local_datetime():
    return localtime()


class CommonExp(models.Model):    
    e_id = models.AutoField(primary_key=True)  # assuming it's an auto-increment id
    e_day = models.DateField()                  # assuming this is a date
    esubcode = models.CharField(max_length=50) # adjust max_length as needed
    ex_cost = models.DecimalField(max_digits=10, decimal_places=2)  # cost field
    EDescribe = models.TextField()              # description, can be TextField
    ExpdBy = models.ForeignKey("ProjectAdmin.Employee",on_delete=models.CASCADE)  # name or code of person who expended
    pic = models.ImageField(upload_to='commonexp_pics/', blank=True, null=True)  # optional picture
    
    myuser = models.CharField(max_length=100)  # user who entered data, or FK if you want
    mm = models.IntegerField()                  # month? (adjust type)
    rtime = models.DateTimeField(default=current_local_datetime)         # recorded time
    status = models.CharField(default='Pending',max_length=30)   # status field, could be choices
    dy = models.ForeignKey("ProjectAdmin.DealingYear", on_delete=models.CASCADE)                  # day? (adjust type)
    com_id = models.ForeignKey("ProjectAdmin.Company", on_delete=models.CASCADE)


    def __str__(self):
        return f"CommonExp {self.e_id} - {self.EDescribe[:20]}"

    class Meta:
        db_table = 'commonexp'  # map to existing table


 
class HeadExp(models.Model):
    head_code = models.CharField(max_length=10,primary_key=True)
    head_name = models.CharField(max_length=100, unique=True)
    
    
    def __str__(self):
        return self.head_name   # 👈 This makes the dropdown readable


class SubHead(models.Model):
    sub_hcode = models.ForeignKey(HeadExp,on_delete=models.CASCADE)
    sub_code = models.CharField(primary_key=True, max_length=15)
    subhead_name = models.CharField(max_length=100,unique=True)
    
    
    def __str__(self):
        return self.subhead_name   # 👈 This makes the dropdown readable

from django.contrib.auth.models import User
class BlockName(models.Model):    
    b_id = models.CharField(max_length=20,  primary_key=True)
    b_name = models.CharField(max_length=100,unique=True)
    b_land_Ac = models.FloatField()
    PerDecimal = models.DecimalField(max_digits=10, decimal_places=2)
    b_des = models.TextField(blank=True, null=True)
    division = models.CharField(max_length=20, choices=[
        ('AC', 'Account'),
        ('SP', 'Seed Production'),
        ('SM', 'Seed Marketing')
    ], default='AC')
    bso_email = models.EmailField()
    state = models.CharField(max_length=10, choices=[('ON', 'ON'), ('OFF', 'OFF')], default='ON')
    rlpay_day = models.CharField(max_length=50, default='Sunday')
    land_update = models.DecimalField(max_digits=10, decimal_places=2)
    division = models.CharField(max_length=20, choices=DIVISION_CHOICES, default='AC')
    emailst = models.EmailField()
    com_id = models.ForeignKey("ProjectAdmin.Company", on_delete=models.CASCADE)

    
    def save(self, *args, **kwargs):
        if not self.b_id:
            last = BlockName.objects.order_by('-b_id').first()
            if last:
                num = int(last.b_id[1:]) + 1
            else:
                num = 1
            self.b_id = f"B{num:03d}"  # B001, B002, ...
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.b_id} - {self.b_name}"


class Advance(models.Model):
    date = models.DateField()
    receiver = models.ForeignKey("ProjectAdmin.Employee", on_delete=models.CASCADE, default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    abrief = models.CharField(max_length=200)
    target_file = models.FileField(upload_to='advance_files/')
    rtime = models.DateTimeField(auto_now=True)
    entrier = models.CharField(max_length=20,default='admin_user')
    byear = models.ForeignKey("ProjectAdmin.DealingYear", on_delete=models.CASCADE, default=1)
    com_id = models.ForeignKey("ProjectAdmin.Company", on_delete=models.CASCADE, default=1)

    def __str__(self):
        return str(self.receiver)
     

class UserProfile(models.Model):
    STATUS_CHOICES = [
        ('Stop', 'Stop'),
        ('On', 'On'),
        ('Abuse', 'Abuse'),
    ]
    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True, blank=True)
    block_id  = models.ForeignKey(BlockName, on_delete=models.CASCADE)
    status = models.CharField(
    max_length=40,
    choices=STATUS_CHOICES,
    default='On'
    )  
    ALLOWED_APPS = [
        ('account', 'Account'),
        ('block', 'Block'),
        ('marketing', 'Marketing'),
        ('contract_grower', 'Contract_grower'),
        ('ProjectAdmin', 'ProjectAdmin'),
    ]

    allowed_app = models.CharField(max_length=100, choices=ALLOWED_APPS)

    byear  = models.ForeignKey(DealingYear, on_delete=models.CASCADE,null=True, blank=True)
    com_id = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} ({self.allowed_app})"