from django import forms
from ProjectAdmin.models import Catagory
from account.models import Advance, SubHead
import os

class advanceEntryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # view থেকে employee parameter pop করা
        self.employee = kwargs.pop('employee', None)
        super().__init__(*args, **kwargs)

        # সব fields এ Bootstrap class ensure করা
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Advance
        fields = ['date', 'amount', 'abrief', 'target_file']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select Date'
            }),
            'receiver': forms.HiddenInput(),  # hidden, value set in view
            'amount': forms.NumberInput(attrs={
                'placeholder': 'Enter Amount',
                'step': '0.01',
                'class': 'form-control'
            }),
            'abrief': forms.Textarea(attrs={
                'placeholder': 'Enter description (optional)',
                'class': 'form-control',
                'rows': 2
            }),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            raise forms.ValidationError("Amount একটি বৈধ সংখ্যা হতে হবে।")
        if amount <= 0:
            raise forms.ValidationError("Amount অবশ্যই 0-এর বেশি হতে হবে।")
        return amount

    def clean_target_file(self):
        file = self.cleaned_data.get('target_file')
        if file:
            if file.size > 5 * 1024 * 1024:  # 5MB max
                raise forms.ValidationError("File size must be under 5MB.")

            valid_extensions = ['.pdf', '.docx', '.xlsx', '.jpg']
            ext = os.path.splitext(file.name)[1]
            if ext.lower() not in valid_extensions:
                raise forms.ValidationError("Allowed file types: pdf, docx, xlsx, jpg.")
        return file

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        amount = cleaned_data.get('amount')
        receiver = self.employee  # view থেকে passed employee

        if date and receiver and amount:
            exists = Advance.objects.filter(
                date=date,
                receiver=receiver,
                amount=amount
            ).exists()
            if exists:
                raise forms.ValidationError(
                    "এই তারিখ, রিসিভার এবং অ্যামাউন্টের combination ইতিমধ্যেই আছে।"
                )
        return cleaned_data


from .models import Budget, LandMeasure, SeedTransport

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        exclude = ['block_id', 'byear', 'com_id', 'user']  # auto-set fields

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # logged-in user
        super().__init__(*args, **kwargs)

        if user:
            # Get already used sub_codes for this user
            used_sub_codes = Budget.objects.filter(user_id=user).values_list('sub_code', flat=True)

            # Filter sub_code field to exclude used ones
            self.fields['sub_code'].queryset = SubHead.objects.exclude(id__in=used_sub_codes)


from django import forms
from .models import Person


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        
        # Auto-set fields: user, person_id, block_id, com_id, created_at
        exclude = ['user', 'person_id', 'block_id', 'com_id', 'created_at']

        widgets = {
            'catagory_short': forms.Select(attrs={'class': 'form-select'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'nid_no': forms.TextInput(attrs={'class': 'form-control'}),           
            'mobile_no': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dropdown label: show short code + full name
        self.fields['catagory_short'].label_from_instance = lambda obj: f"{obj.catagory_short} - {obj.catagoryName}"
        # Save only short code (to_field_name)
        self.fields['catagory_short'].to_field_name = 'catagory_short'

        # Person Picture & NID Picture optional
        self.fields['person_picture'].required = False
        self.fields['person_nid_picture'].required = False

         # Edit mode: make catagory_short readonly (disabled)
        if self.instance and self.instance.pk:
            self.fields['catagory_short'].disabled = True
    
    def clean(self):
        cleaned_data = super().clean()
        catagory_short = cleaned_data.get("catagory_short")
        mobile_no = cleaned_data.get("mobile_no")

        # Prevent duplicate catagory + mobile number
        qs = Person.objects.filter(catagory_short=catagory_short, mobile_no=mobile_no)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)  # exclude current instance in edit mode

        if catagory_short and mobile_no and qs.exists():
            raise forms.ValidationError(
                "⚠️ এই ক্যাটাগরি এবং মোবাইল নম্বর দিয়ে একটি রেকর্ড আগে থেকেই আছে।"
            )
        return cleaned_data


    # Validation for mobile number
    def clean_mobile_no(self):
        mobile = self.cleaned_data.get('mobile_no')
        if mobile and not mobile.isdigit():
            raise forms.ValidationError("Mobile number must contain digits only.")
        return mobile

    # Validation for NID number
    def clean_nid_no(self):
        nid = self.cleaned_data.get('nid_no')
        if nid and not nid.isdigit():
            raise forms.ValidationError("NID number must contain digits only.")
        return nid



class LandMeasureForm(forms.ModelForm):
    class Meta:
        model = LandMeasure
        fields = ['edate', 'llid', 'plot_no', 'length1', 'length2', 'width1', 'width2']

        widgets = {
            'edate': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select Date'
            }),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # # Get LL category object
        # try:
        #     ll_category = Catagory.objects.get(catagory_short="LL")
        #     self.fields['llid'].queryset = Person.objects.filter(catagory_short=ll_category)
        # except Catagory.DoesNotExist:
        #     self.fields['llid'].queryset = Person.objects.none()  # empty queryset if LL not found

        # print(f"LL Persons queryset: {self.fields['llid'].queryset}")
        
        # self.fields['llid'].empty_label = "Select Person"
        
        ll_category = Catagory.objects.get(catagory_short="LL")
        self.fields['llid'].queryset = Person.objects.filter(catagory_short=ll_category)
        self.fields['llid'].empty_label = "Select Person"
        self.fields['llid'].widget.attrs.update({'class': 'form-select'})  # select style



        # Bootstrap class
        for field in self.fields.values():
            if field.widget.__class__.__name__ != 'CheckboxInput':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'

class SeedTransportForm(forms.ModelForm):
    class Meta:
        model = SeedTransport
        fields = [
            "sending_date",            
            "chalan_no",
            "seed_sent",
            "seed_received",
            "empty_bags",
            "variety_name",
            "driver_name" 
        ]

        exclude = ['b_id','departure_time','arrival_time','duration','com_id']

        widgets = {
            "sending_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),            
            "chalan_no": forms.TextInput(attrs={"class": "form-control"}),
            "seed_sent": forms.NumberInput(attrs={"class": "form-control"}),
            "seed_received": forms.NumberInput(attrs={"class": "form-control"}),
            "empty_bags": forms.NumberInput(attrs={"class": "form-control"}),
            "variety_name": forms.Select(attrs={'class': 'form-select'}),
            "driver_id": forms.TextInput(attrs={"class": "form-control"}),     
           
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        
        ll_category = Catagory.objects.get(catagory_short="DRV")
        self.fields['driver_id'].queryset = Person.objects.filter(catagory_short=ll_category)
        self.fields['driver_id'].empty_label = "Select Person"
        self.fields['driver_id'].widget.attrs.update({'class': 'form-select'})  # select style   