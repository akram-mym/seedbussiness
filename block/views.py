import re
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from ProjectAdmin.models import Catagory, Employee
from block.forms import  advanceEntryForm,Budget
from account.models import Advance, UserProfile



# Create your views here.
def home(request):
    return render(request, 'block/base_block.html')

def success_advance(request):
    return render(request, 'block/success.html', {'message': 'Advance saved successfully!'})  

def userlist(request):
    # profiles = UserProfile.objects.select_related('user', 'userid').all()
    profiles = UserProfile.objects.all()
    return render(request,'block/userlist.html', {'profiles' : profiles})

def advance_insert(request):
    if request.method == 'POST':
        employee = request.user.userprofile.userid
        form = advanceEntryForm(request.POST, request.FILES, employee=employee)
        if form.is_valid():
            instance = form.save(commit=False)
            user = request.user
            instance.byear = user.userprofile.byear
            instance.com_id = user.userprofile.com_id
            instance.rtime = timezone.now()
            instance.receiver = user.userprofile.userid
            instance.entrier = user.userprofile.userid
            instance.save()            
            return redirect('block:advance_info')
    else:
        form = advanceEntryForm()
        
    return render(request, 'block/advance_insert.html', {'form': form})

def advance_info(request):
    # লগইন ইউজারের UserProfile বের করি
    profile = get_object_or_404(UserProfile, user=request.user)

    # UserProfile থেকে Employee বের করি
    employee = profile.employee_id  

    # সেই Employee এর জন্য Advance ফিল্টার করি
    advances = Advance.objects.filter(receiver=employee)

    context = {
        'advances': advances,
    }
    return render(request, 'block/advance/advance_info.html', context)


from block.forms import BudgetForm

def budget_insert(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            profile = request.user.userprofile
            obj.block_id = profile.block_id   # assuming user has this field
            obj.user_id = profile.user_id
            obj.byear = request.user.userprofile.byear
            obj.com_id = request.user.userprofile.com_id
            obj.save()
            return redirect('block:budget_list')  # <-- budget list view
    else:
        form = BudgetForm()
    return render(request, 'block/budget/budget_form.html', {'form': form})



def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'block/budget/budget_list.html', {'budgets': budgets})
    

# def budget_edit(request, pk):
#     """
#     Edit an existing Budget entry.
#     """
#     budget = get_object_or_404(Budget, pk=pk)

#     if request.method == "POST":
#         form = BudgetForm(request.POST, instance=budget)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Budget updated successfully.")
#             return redirect('block:budget_list')
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = BudgetForm(instance=budget)

#     return render(request, 'block/budget/budget_form.html', {'form': form, 'budget': budget})

def update_record(request, pk):
    record = get_object_or_404(Budget, pk=pk, user=request.user)

    if request.method == "POST":
        form = BudgetForm(request.POST, instance=record)
        if form.is_valid():
            budget = form.save(commit=False)
            # ✅ keep values tied to logged-in user
            budget = form.save(commit=False)
            # Keep logged-in user fields intact
            budget.user = request.user
            if hasattr(request.user.userprofile, 'block_id'):
                budget.block_id = str(request.user.userprofile.block_id)
            if hasattr(request.user.userprofile, 'byear'):
                budget.byear = str(request.user.userprofile.byear)
            if hasattr(request.user.userprofile, 'com_id'):
                budget.com_id = str(request.user.userprofile.com_id)
            budget.save()            
            return redirect('block:budget_list')
    else:
        form = BudgetForm(instance=record)
    return render(request, 'block/budget/budget_form.html', {'form': form})

import re
from django.shortcuts import render, redirect
from .models import LandMeasure, Person
from .forms import LandMeasureForm, PersonForm
from django.contrib.auth.decorators import login_required


from django.db import transaction

@login_required
def create_person(request):
    if request.method == "POST":
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():  # ট্রানজাকশন শুরু
                person = form.save(commit=False)

                # ফর্ম থেকে Catagory object এবং তার short code নেওয়া হচ্ছে
                cat_obj = form.cleaned_data['catagory_short']
                cat_short = cat_obj.catagoryshort  # যেমন: 'LL'

                # ওই user + ওই category এর শেষ person লক সহ খোঁজা হচ্ছে
                last_person = (
                    Person.objects
                    .select_for_update()   # লক করবে, যাতে অন্য কেউ একসাথে লিখতে না পারে
                    .filter(
                        user=request.user,
                        person_id__startswith=cat_short + "_"
                    )
                    .order_by('-id')
                    .first()
                )

                # নতুন সিরিয়াল বের করা
                if last_person and last_person.person_id and re.match(r'^.*_\d+$', last_person.person_id):
                    prefix, number = last_person.person_id.split('_')
                    new_number = int(number) + 1
                else:
                    new_number = 1

                # নতুন person_id তৈরি (যেমন: LL_0001)
                person.person_id = f"{cat_short}_{new_number:04d}"

                # Auto-fill fields
                person.user = request.user        
                person.block_id = request.user.userprofile.block_id
                person.com_id = request.user.userprofile.com_id

                person.save()

                messages.success(request, "✅ নতুন ব্যক্তির তথ্য সফলভাবে যোগ হয়েছে।")
                return redirect('block:person_list')
        
    else:
        form = PersonForm()

    return render(request, 'block/person/create_person.html', {'form': form})



from .models import Person
from django.db.models import Q
from django.core.paginator import Paginator

def person_list(request):
    query = request.GET.get('q', '')

    # Filter only logged-in user's persons
    persons = Person.objects.filter(user=request.user)

    if query:
        persons = persons.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(person_id__icontains=query) |
            Q(father_name__icontains=query) |
            Q(mobile_no__icontains=query) |
            Q(catagory_short__catagoryshort__icontains=query) |
            Q(catagory_short__catagoryName__icontains=query)
        )

    persons = persons.order_by('-created_at')

    # Pagination: 10 per page
    paginator = Paginator(persons, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query
    }
    return render(request, 'block/person/person_list.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .forms import PersonForm
from .models import Person

# Edit person
def person_edit(request, pk):
    person = get_object_or_404(Person, pk=pk, user=request.user)

    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        try:
            if form.is_valid():
                with transaction.atomic():
                    person_instance = form.save(commit=False)

                    # Keep original catagory_short
                    person_instance.catagory_short = person.catagory_short

                    # Auto-fill hidden fields
                    person_instance.user = request.user
                    person_instance.block_id = getattr(request.user, 'block_id', person_instance.block_id)
                    person_instance.com_id = getattr(request.user, 'com_id', person_instance.com_id)

                    person_instance.save()
                    messages.success(request, "✅ ব্যক্তির তথ্য সফলভাবে আপডেট হয়েছে।")
                    return redirect('block:person_list')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except Exception as e:
            messages.error(request, f"⚠️ কিছু সমস্যা হয়েছে: {str(e)}")

        # Render form with errors if invalid
        return render(request, 'block/person/person_form.html', {'form': form, 'person': person})

    else:
        form = PersonForm(instance=person)
        return render(request, 'block/person/person_edit.html', {'form': form, 'person': person})
    

def landmeasure_list(request):
    landmeasures = LandMeasure.objects.all().order_by('-edate')
    return render(request, 'block/land/landmeasure_list.html', {'landmeasures': landmeasures})


def calculate_deci(length1, length2, width1, width2):
    ld1 = (length1 + length2) / 2
    ld2 = (width1 + width2) / 2
    deci = (ld1 * ld2) / 40.478
    return round(deci, 2)



@login_required
def landmeasure_create(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        form = LandMeasureForm(request.POST)
        if form.is_valid():
            landmeasure = form.save(commit=False)

            # Auto-fill fields
            landmeasure.b_id = user_profile.block_id.id if user_profile.block_id else 0
            landmeasure.com_id = user_profile.com_id.id if user_profile.com_id else 0
            landmeasure.state = "ON"
            landmeasure.plot_no = request.GET()

            # Auto-calculate deci
            landmeasure.deci = calculate_deci(
                float(landmeasure.length1),
                float(landmeasure.length2),
                float(landmeasure.width1),
                float(landmeasure.width2)
            )

            landmeasure.save()
            return redirect("landmeasure_list")
    else:
        form = LandMeasureForm()

        # Limit llid queryset to LL category Persons
        try:
            ll_category = Catagory.objects.get(catagoryName="LL")
            form.fields['llid'].queryset = Person.objects.filter(catagory_short=ll_category)
        except Catagory.DoesNotExist:
            form.fields['llid'].queryset = Person.objects.none()    

    return render(request, "block/land/landmeasure_form.html", {"form": form})
    


def landmeasure_edit(request, pk):
    landmeasure = get_object_or_404(LandMeasure, pk=pk)
    if request.method == 'POST':
        form = LandMeasureForm(request.POST, instance=landmeasure)
        if form.is_valid():
            form.save()
            return redirect('landmeasure_list')
    else:
        form = LandMeasureForm(instance=landmeasure)
    return render(request, 'block/land/landmeasure_form.html', {'form': form})