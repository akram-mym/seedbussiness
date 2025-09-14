import os
import re
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from ProjectAdmin.models import Catagory
from block.forms import  advanceEntryForm,Budget
from account.models import Advance, UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from seedbussiness import settings
from .forms import PersonForm
from .models import Person
from block.forms import BudgetForm
from .models import Person
from django.db.models import Q
from django.core.paginator import Paginator
import re
from django.shortcuts import render, redirect
from .models import LandMeasure, Person, SeedTransport
from .forms import LandMeasureForm, PersonForm, SeedTransportForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'block/base_block.html')

def success_advance(request):
    return render(request, 'block/success.html', {'message': 'Advance saved successfully!'})  

def userlist(request):
    # profiles = UserProfile.objects.select_related('user', 'employee_id').all()
    profiles = UserProfile.objects.all()
    return render(request,'block/userlist.html', {'profiles' : profiles})

def advance_file_path(instance, filename):
    """
    Upload file to 'advances/' folder, renamed according to advance ID after save.
    """
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = f"advance_{instance.pk}.{ext}"
    else:
        timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
        filename = f"advance_temp_{timestamp}.{ext}"
    return os.path.join('advances', filename)

def advance_insert(request):
    if request.method == 'POST':
        employee = request.user.userprofile.employee_id
        form = advanceEntryForm(request.POST, request.FILES, employee=employee)
        if form.is_valid():
            instance = form.save(commit=False)
            user = request.user
            instance.byear = user.userprofile.byear
            instance.com_id = user.userprofile.com_id
            instance.rtime = timezone.now()
            instance.receiver = user.userprofile.employee_id
            instance.entrier = user.userprofile.employee_id
            instance.email = user.userprofile.employee_id.EmpEmail  
                                       
            # Rename file according to ID if file uploaded
            if instance.target_file:
                ext = instance.target_file.name.split('.')[-1]
                new_filename = f"advance_{instance.pk}.{ext}"
                old_path = instance.target_file.path
                new_path = os.path.join(settings.MEDIA_ROOT, 'advances', new_filename)
                os.rename(old_path, new_path)
                instance.target_file.name = os.path.join('advances', new_filename)
                instance.save(update_fields=['target_file'])
            # Debug prints
            # print(f"Employee Email: {instance.email}")            
            # print(f"Company Email: {user.userprofile.com_id.company_email}")

            # Save the instance
            instance.save()

            # Debug prints
            # print(f"Employee Email: {instance.email}")            
            # print(f"Company Email: {user.userprofile.com_id.company_email}")

            # ----------------------
            # HTML Email
            subject = "Advance Entry Confirmation"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_emails = [instance.email, user.userprofile.com_id.company_email]

            html_content = f"""
            <html>
            <body>
                <p>Dear <strong>{user.username}</strong>,</p>
                <p>Your advance entry has been successfully recorded.</p>
                <ul>
                    <li><strong>Employee Email:</strong> {instance.email}</li>
                    <li><strong>Company Email:</strong> {user.userprofile.com_id.company_email}</li>
                    <li><strong>Entry Date:</strong> {request.POST.get('date')}</li>
                    <li><strong>Amount:</strong> {request.POST.get('amount')}</li>
                    <li><strong>Recorded Time:</strong> {instance.rtime.strftime('%Y-%m-%d %H:%M')}</li>
                </ul>
                <p>Thank you,<br/>Seed Business Team</p>
            </body>
            </html>
            """

            try:
                msg = EmailMultiAlternatives(subject, "", from_email, to_emails)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                # print("✅ HTML Email sent successfully to employee + company")
            except Exception as e:
                print(f"❌ Email sending failed: {e}")

            return redirect('block:advance_info')

        else:
            # Form invalid হলে
            print("Form errors:", form.errors)
            return render(
                request,
                'block/advance_insert.html',
                {'form': form, 'errors': form.errors}
            )
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
                cat_short = cat_obj.catagory_short  # যেমন: 'LL'

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
            landmeasure.b_id = user_profile.block_id if user_profile.block_id else 0
            landmeasure.com_id = user_profile.com_id if user_profile.com_id else 0
            landmeasure.state = "ON"
            
            # Format plot_no => P + 3 digits
            raw_plot_no = request.POST.get("plot_no", "").strip()
            if raw_plot_no:
                # Remove leading P if user typed it
                if raw_plot_no.upper().startswith("P"):
                    raw_plot_no = raw_plot_no[1:]

                # Ensure it's numeric and 3 digits
                try:
                    num = int(raw_plot_no)
                    landmeasure.plot_no = f"P{str(num).zfill(3)}"   # e.g. P001, P045, P123
                except ValueError:
                    # fallback if not numeric
                    landmeasure.plot_no = "P000"
            else:
                landmeasure.plot_no = "P000"

            # Auto-calculate deci
            landmeasure.deci = calculate_deci(
                float(landmeasure.length1),
                float(landmeasure.length2),
                float(landmeasure.width1),
                float(landmeasure.width2)
            )

            landmeasure.save()
            return redirect("block:landmeasure_list")
    else:
        form = LandMeasureForm()

        # Limit llid queryset to LL category Persons
        try:
            ll_category = Catagory.objects.get(catagory_short="LL")
            print(f"Person Id :{ ll_category}")
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

@login_required
def seed_transport_create(request):
    """Create a new SeedTransport entry."""
    if request.method == "POST":
        form = SeedTransportForm(request.POST)
        if form.is_valid():
            seed_transport = form.save(commit=False)

            # Auto-fill from UserProfile
            user = request.user
            try:
                profile = UserProfile.objects.get(user=user)
                seed_transport.com_id = profile.com_id   # adjust field name
                seed_transport.b_id = profile.block_id  
                seed_transport.byear = profile.byear       # adjust field name
                seed_transport.departure_time = timezone.now()
                seed_transport.seed_received = request.POST.get('seed_sent')

                # Copy seed_sent → seed_received (cast to int)
                seed_sent_value = request.POST.get("seed_sent")
                if seed_sent_value:
                    seed_transport.seed_received = int(seed_sent_value)

                # Debug log (safe f-string)
                print(
                    f"com_id: {seed_transport.com_id}, "
                    f"b_id: {seed_transport.b_id}, "
                    f"byear: {seed_transport.byear}, "
                    f"seed_received: {seed_transport.seed_received}"
                )
                
            except UserProfile.DoesNotExist:
                seed_transport.com_id = None
                seed_transport.b_id = None
              # You could also auto-calculate duration if departure/arrival exist later
            seed_transport.save()
            return redirect("block:seed_transport_list")
    else:
        form = SeedTransportForm()

    return render(request, "block/seedtransort/seed_transport_form.html", {"form": form})


@login_required
def seed_transport_list(request):
    """Show all SeedTransport records."""
    records = SeedTransport.objects.all().order_by("-sending_date")
    return render(request, "block/seedtransort/seed_transport_list.html", {"records": records})