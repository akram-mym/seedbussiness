import datetime
from pyexpat.errors import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from ProjectAdmin.forms import EmployeeInfoEntry
from ProjectAdmin.models import Employee

from ProjectAdmin.models import  Company
# from account.forms import BlockNameForm
from account.forms import   EmployeeForm, HeadExpForm, UserProfileForm
from django.shortcuts import render, redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class HomeView(LoginRequiredMixin, TemplateView):
    login_url = 'login'  # লগইন পেজের URL নাম
    template_name = 'account/home.html'




# Create your views here.

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             messages.success(request, f"Welcome, {user.username}!")
#             return redirect(f'/{user.userprofile.allowed_app}/')
#         else:
#             messages.error(request, "Invalid username or password.")

#     return render(request, 'account/login.html')

def homepage(request):

    return render(request, 'account/account1.html')

def account(request):
    context = {"key" : "I am Akram"}
    return render(request, 'account/account.html', context=context)

def book(request):
    context = {"ID" : "SBID0123",
               "Name" : "Histry of World",
               "Auth" : "Akram",
               "Publi" : "2016",
               }
    return render(request, 'account/book.html', context=context)

def teacher_name(request):
    names = ["Akram", "Rahim", "Karim", "Moynal" ]
              
    order = request.GET.get('order', 'ASC')
    
    if order.upper() == "ASC":
        names.sort()
    elif order.upper() == "DESC":
        names.sort(reverse=True)


    return render(request, 'account/name.html', { 'context1' : names} )

# def block_entry(request):
#     block = BlockName.objects.all()
#     return render(request, 'account/block_form.html', {'form':  block })

def block_info(request):
    block = BlockName.objects.all()
    return render(request, 'account/block_info.html', {'block_list':  block })

# views.py


def com_info(request):
    com = Company.objects.all()
    return render(request, 'account/com_info.html', {'comp_list':  com })

from django.shortcuts import render

def success_page(request):
    return render(request, 'account/success_page.html')

def my_view(request):
        # সেশন থেকে ডেটা পড়া
    visits = request.session.get('visits', 0)
    request.session['visits'] = visits + 1
    return HttpResponse(f"You have visited this page {visits} times.")



def blockname_list(request):
    blocks = BlockName.objects.all()
    return render(request, 'account/blockname_list.html', {'blocks': blocks})


def success_page_emp(request):
    return render(request, 'account/success_page_emp.html', {'message': 'Company saved successfully!'})  

def success_emp(request):
    return render(request, 'account/success_page_emp.html', {'message': 'Employee saved successfully!'})  

def EmployeeInfoEntryView(request):
    if request.method == 'POST' :
        form = EmployeeInfoEntry(request.POST, request.FILES)  # ✅ গুরুত্বপূর্ণ
        if form.is_valid(): 
            form.save()
            return redirect('account:success_emp')

        else:
            print(form.errors)

    else:
        form = EmployeeInfoEntry()    
    return render(request, 'account/EmpInfoEntry.html', {'form' : form })        


def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'account/employee_info.html', {
        'employees': employees,
        'form': EmployeeForm(),
        'action_url': '',  # Create action URL (handled in same view)
        'submit_text': 'Create',
    })

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('account:employee_list')
    else:
        form = EmployeeForm()
    employees = Employee.objects.all()
    return render(request, 'account/employee_info.html', {
        'employees': employees,
        'form': form,
        'action_url': request.path,
        'submit_text': 'Create',
    })

def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            print("✅ Employee updated:", form.cleaned_data)
            return redirect('account:employee_list')
        else:
            print("❌ Form errors:", form.errors)
    else:
        form = EmployeeForm(instance=employee)
    employees = Employee.objects.all()
    return render(request, 'account/employee_info.html', {
        'employees': employees,
        'form': form,
        'action_url': request.path,
        'submit_text': 'Update',
    })


def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('account:employee_info')
    # যদি GET method এ delete page দেখতে চান, এখানে template return করুন,
    # নাহলে redirect করে দিন employee list-এ
    return redirect('account:employee_list')


from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import CommonExpForm,advanceEntryForm,SubHeadForm
from django.contrib import messages

# Assuming these are imported or created elsewhere
from .models import  BlockName, CommonExp, Company, HeadExp,Advance, UserProfile  # or wherever they are defined
from ProjectAdmin.models import Employee, DealingYear

def insert_common_exp(request):
    if request.method == 'POST':
        form = CommonExpForm(request.POST, request.FILES)
        if form.is_valid():           
            instance = form.save(commit=False)            
            instance.rtime = timezone.now()
            # Current month as integer (1–12)
            instance.mm = datetime.date.today().month  
            # Use request.user
            user = request.user            
            # Assuming userprofile has b_id field, set FK properly
            
            instance.com_id = user.userprofile.com_id
            instance.dy = user.userprofile.byear
            # If you want to set who entered this:
            instance.myuser = user.username 
            instance.save()
            messages.success(request, "Expense inserted successfully.")
            return redirect('account:insert_common_exp')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CommonExpForm()

    return render(request, 'account/insert_common_exp.html', {'form': form})
    
# def common_exp_report(request):
#     expenses = CommonExp.objects.select_related('ExpdBy', 'b_id', 'dy', 'com_id').all()
#     return render(request, 'account/common_exp_report.html', {'expenses': expenses})

from django.db.models import Sum

def common_exp_report(request):
    expenses = CommonExp.objects.select_related('ExpdBy',  'dy', 'com_id').all()

    expenses_by_subcode = (
        expenses
        .values('esubcode')
        .annotate(total_cost=Sum('ex_cost'))
        .order_by('esubcode')
    )
    # Prepare data for Chart.js
    labels = [item['esubcode'] for item in expenses_by_subcode]
    totals = [float(item['total_cost']) for item in expenses_by_subcode]


    return render(request, 'account/common_exp_report.html', {
        'expenses': expenses,
        'expenses_by_subcode': expenses_by_subcode,
        'labels': labels,
        'totals': totals,
    })

# HeadExp Table 
# Insert View
def insert_head_exp(request):
    if request.method == 'POST':
        form = HeadExpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "HeadExp সফলভাবে যোগ হয়েছে।")
            return redirect('account:insert_head_exp')  # adjust this to your actual URL name
    else:
        form = HeadExpForm()
    return render(request, 'account/insert_head_exp.html', {'form': form})


# Update View
def update_head_exp(request, pk):  # pk = head_name
    head = get_object_or_404(HeadExp, pk=pk)
    if request.method == 'POST':
        form = HeadExpForm(request.POST, instance=head)
        if form.is_valid():
            form.save()
            messages.success(request, "HeadExp সফলভাবে আপডেট হয়েছে।")
            return redirect('head_exp_list')  # redirect to list page or another view
    else:
        form = HeadExpForm(instance=head)
    return render(request, 'account/update_head_exp.html', {'form': form, 'head': head})


def view_head_exp(request):
    heads = HeadExp.objects.all()
    return render(request, 'account/view_head_exp.html', {'heads': heads})


def subhead_entry(request):
    if request.method == 'POST':
        form = SubHeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"SubHead সফলভাবে যোগ হয়েছে।")
            return redirect('account:subhead')
    else:
        form = SubHeadForm()
    return render(request,'account/subhead.html', {'form' : form})    



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm



def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():

            # 1️⃣ Save Django User
            new_user = user_form.save()

            # 2️⃣ Save UserProfile
            user_profile = profile_form.save(commit=False)
            user_profile.user = new_user
            user_profile.save()

            messages.success(request, '✅ Registration successful! You can now login.')
            return redirect('account:login')
        else:
            print(user_form.errors)
            print(profile_form.errors)
    else:
        user_form = UserCreationForm()
        # profile_form = UserProfileForm()

    return render(request, 'account/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })




def save(self, commit=True):
    user = super().save(commit=False)
    if commit:
        user.save()
    print("Cleaned Data:", self.cleaned_data)  # Check these values
    user_profile = UserProfile(
        user=user,
        userid=self.cleaned_data['userid'],
        b_id=self.cleaned_data['b_id'],
        status=self.cleaned_data['status'],
        byear=self.cleaned_data['byear'],
        com_id=self.cleaned_data['com_id'],
    )
    if commit:
        user_profile.save()
    return user


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('account:home')  # Change 'home' to your actual homepage route name
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'account/login.html')

def custom_logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('account:login')  # Redirect to login page with message



def advance_insert(request):
    if request.method == 'POST':
        form = advanceEntryForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            user = request.user
            instance.byear = user.userprofile.byear
            instance.com_id = user.userprofile.com_id
            instance.rtime = timezone.now()
            instance.entrier = user.userprofile.userid
            instance.save()
            messages.success(request, 'Advance Entry is Successful.')
            return redirect('account:home')
    else:
        form = advanceEntryForm()
        
    return render(request, 'account/advance_insert.html', {'form': form})


def advance_info(request):
    advances = Advance.objects.all()  # সব Advance রেকর্ড নিয়ে আসবে
    context = {
        'advances': advances,
    }
    return render(request, 'account/advance_info.html', context)

def advance_edit(request, pk):
    instance = get_object_or_404(Advance, pk=pk)
    if request.method == 'POST':
        form = advanceEntryForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Advance entry updated successfully.")
            return redirect('account:advance_info')  # Update with your list view name
    else:
        form = advanceEntryForm(instance=instance)
    return render(request, 'account/advance_edit.html', {'form': form})

def userprofile_view(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, "account/userprofile.html", {"profile": profile})
    # return render(request, "account/userprofile.html", {"profile": profile})