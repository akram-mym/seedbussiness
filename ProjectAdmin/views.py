from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from ProjectAdmin.models import  Catagory, Company, DealingYear

from account.forms import BlockNameUpdateForm,  SubHeadEditForm, SubHeadForm, UserProfileForm,UserProfileListForm1,BlockNameForm
from account.models import Company, SubHead, UserProfile,BlockName
import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import  CatagoryForm, CompanyInfoEntry, DealingYearForm

# Create your views here.
def user(request):
    return HttpResponse (request,'<h1>This is Project Admin.</h1>')
    
def home(request):
    return render(request, 'padmin/base1.html')

def home1(request):
    return render(request, 'padmin/home.html')




def company_entry_view(request):
    if request.method == 'POST':
        form = CompanyInfoEntry(request.POST)
        if form.is_valid():
            company_form =form.save(commit=False)
             # Get all existing com_ids and find the max number
            existing_ids = Company.objects.values_list('com_id', flat=True)
            max_number = 0
            for cid in existing_ids:
                try:
                    num = int(cid.split('_')[1])
                    if num > max_number:
                        max_number = num
                except (IndexError, ValueError):
                    continue

            new_number = max_number + 1
            company_form.com_id = f"Com_{new_number:03d}"


            company_form.save()
            return redirect('ProjectAdmin:success_page')  # success_page আপনার URL name
        else:
            print(form.errors)  # ⚠️ Debugging এর জন্য
    else:
        form = CompanyInfoEntry()
        
    return render(request, 'padmin/com_info_entry.html', {'form': form})
     
def com_info(request):
    com = Company.objects.all()
    return render(request, 'padmin/dealing_year/com_info.html', {'comp_list':  com })
   
def company_update_view(request, com_id):
    company = get_object_or_404(Company, pk=com_id)
    if request.method == 'POST':
        form = CompanyInfoEntry(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = CompanyInfoEntry(instance=company)
    return render(request, 'padmin/company_info_entry.html', {'form': form, 'update': True})

def search_company(request):

    company = Company.objects.all()
    query = request.GET.get('q','')
    
    if query:            
            company = company.filter(
                Q(company_name__icontains = query) | 
                Q(company_email__icontains = query)
            )
    context = {
                'company' : company,
                'query' : query
            }
    return render(request,'padmin/search_company.html', context)

def success_view(request):
    return render(request, 'padmin/success_page.html', {'message': 'Company saved successfully!'})

from django.contrib.auth.forms import UserCreationForm

def CreateUser(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileListForm1(request.POST)

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
        profile_form = UserProfileListForm1()

    return render(request, 'padmin/CreateUser.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

def userlist(request):
    # profiles = UserProfile.objects.select_related('user', 'userid').all()
    profiles = UserProfile.objects.all()
    return render(request,'padmin/userlist.html', {'profiles' : profiles})




def add_dealing_year(request):
    if request.method == 'POST':
        form = DealingYearForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ProjectAdmin:dealing_year_list')  # অথবা list বা অন্য পেজ
    else:
        form = DealingYearForm()
    
    return render(request, 'padmin/dealing_year/add_byear.html', {'form': form})



# 🔹 List View
def dealing_year_list(request):
    year = DealingYear.objects.all()
    return render(request, 'padmin/dealing_year/list_byear.html', {'years': year})


# 🔹 Edit View
def edit_dealing_year(request, dy_session):
    year = get_object_or_404(DealingYear, dy_session=dy_session)
    if request.method == 'POST':
        form = DealingYearForm(request.POST, instance=year)
        if form.is_valid():
            form.save()
            return redirect('ProjectAdmin:home')
    else:
        form = DealingYearForm(instance=year)
    return render(request, 'padmin/dealing_year/edit_dealing_year.html', {'form': form})


# 🔹 Delete View
def delete_dealing_year(request, dy_session):
    year = get_object_or_404(DealingYear, dy_session=dy_session)
    if request.method == 'POST':
        year.delete()
        return redirect('padmin/dealing_year/list_byear.html')
    return render(request, 'padmin/dealing_year/delete.html', {'year': year})

# def CreateUser(request):
#     pass 
#     # form = EmployeeInfoEntry()
#     # return redirect(request,'padmin/CreateUser.html', {'form' : form })




def blockname_entry(request):
    if request.method == 'POST':
        form = BlockNameForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            
            # Auto-generate b_id safely
            last_block = BlockName.objects.order_by('-b_id').first()
            if last_block and last_block.b_id and re.match(r'^B\d+$', last_block.b_id):
                new_number = int(last_block.b_id[1:]) + 1
            else:
                new_number = 1
            instance.b_id = f"B{new_number:04d}"
            instance.save()
            return redirect('ProjectAdmin:blockname_list')
    else:
        form = BlockNameForm()
    return render(request, 'padmin/blockname_entry.html', {'form': form})



def blockname_list(request):
    blocks = BlockName.objects.all()
    return render(request, 'padmin/block_info.html', {'block_list': blocks})
  

def success_block(request):
    return render(request,'padmin/success.html')



def block_update_view(request, pk):
    block = get_object_or_404(BlockName, pk=pk)

    if request.method == 'POST':
        form = BlockNameUpdateForm(request.POST, instance=block)
        if form.is_valid():
            form.save()
            return redirect('ProjectAdmin:block_info')  # অথবা যেকোনো উপযুক্ত success URL
    else:
        form = BlockNameUpdateForm(instance=block)

    return render(request, 'padmin/block_update.html', {'form': form})

def block_delete(request, pk):
    block = get_object_or_404(BlockName, pk=pk)
    if request.method == 'POST':
        block.delete()
        return redirect('padmin:block_info')
    # যদি GET method এ delete page দেখতে চান, এখানে template return করুন,
    # নাহলে redirect করে দিন employee list-এ
    return redirect('ProjectAdmin:block_info')


# CREATE
def Catagory_add(request):
    if request.method == 'POST':
        form = CatagoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.catagoryName = cat.catagoryName.title()  # প্রতিটি শব্দ Capitalized হবে
            cat.save()
            return redirect('ProjectAdmin:catagory_list')
    else:
        form = CatagoryForm()
    return render(request, 'padmin/catagory_add.html', {'form': form})


# READ (List)
def Catagory_list(request):
    catagories = Catagory.objects.all()
    return render(request, 'padmin/catagory_list.html', {'catagories': catagories})


# UPDATE
def Catagory_edit(request, pk):
    catagory = get_object_or_404(Catagory, pk=pk)
    if request.method == 'POST':
        form = CatagoryForm(request.POST, instance=catagory)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.catagoryName = cat.catagoryName.title()  # Update এর সময়ও Capitalized হবে
            cat.save()
            return redirect('ProjectAdmin:catagory_list')
    else:
        form = CatagoryForm(instance=catagory)
    return render(request, 'padmin/catagory_edit.html', {'form': form})


# DELETE
def Catagory_delete(request, pk):
    catagory = get_object_or_404(Catagory, pk=pk)
    if request.method == 'POST':
        catagory.delete()
        return redirect('ProjectAdmin:catagory_list')
    return render(request, 'padmin/catagory_delete.html', {'catagory': catagory})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from account.models import UserProfile
from .forms import UserProfileForm

# List all profiles
# def userprofile_list(request):
#     profiles = UserProfile.objects.all()
#     return render(request, 'padmin/userprofile_list.html', {"profiles": profiles})
def userprofile_list(request):
    """
    Display a list of all UserProfiles with related Employee, Company, Block, and Year.
    """
    profiles = UserProfile.objects.select_related(
        'user', 'employee_id', 'block_id', 'byear', 'com_id'
    ).all()

    context = {
        'profiles': profiles
    }
    return render(request, 'padmin/userprofile_list.html', context)




# View single profile
def userprofile_view(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    return render(request, 'padmin/userprofile_view.html', {"profile": profile})

# Edit profile
def userprofile_edit(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "User profile updated successfully.")
            return redirect('ProjectAdmin:userprofile_list')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'padmin/userprofile_form.html', {"form": form, "profile": profile})

# Delete profile
def userprofile_delete(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    if request.method == "POST":
        profile.delete()
        messages.success(request, "User profile deleted successfully.")
        return redirect('ProjectAdmin:userprofile_list')
    return render(request, "padmin/userprofile_confirm_delete.html", {"profile": profile})

def subheadlist(request):
    """
    Display a list of all SubHead entries with related HeadExp.
    """
    subheads = SubHead.objects.select_related('sub_hcode').all().order_by('sub_code')

    context = {
        'subheads': subheads
    }
    return render(request, 'padmin/subheadlist.html', context)

def subhead_entry(request):
    if request.method == 'POST':
        form = SubHeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"SubHead সফলভাবে যোগ হয়েছে।")
            return redirect('ProjectAdmin:subheadlist')
    else:
        form = SubHeadForm()
    return render(request,'padmin/subheadlist.html', {'form' : form})    

def subhead_edit(request, pk):
    """
    Edit an existing SubHead entry.
    """
    subhead = get_object_or_404(SubHead, pk=pk)

    if request.method == "POST":
        form = SubHeadEditForm(request.POST, instance=subhead)
        if form.is_valid():
            form.save()  # only updates the instance, no duplicates
            messages.success(request, "SubHead updated successfully.")
            return redirect('ProjectAdmin:subheadlist')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SubHeadEditForm(instance=subhead)

    return render(request, 'padmin/subheadedit.html', {'form': form, 'subhead': subhead})

def subhead_delete(request, pk):
    """
    Delete an existing SubHead entry.
    """
    subhead = get_object_or_404(SubHead, pk=pk)

    if request.method == "POST":
        subhead.delete()
        messages.success(request, "SubHead deleted successfully.")
        return redirect('ProjectAdmin:subheadlist')

    # GET request → show confirmation page
    return render(request, 'padmin/subhead_confirm_delete.html', {'subhead': subhead})
