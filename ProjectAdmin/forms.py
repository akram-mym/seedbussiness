from django import forms

from .models import Catagory, Company, DealingYear, Employee, hvariety

class CompanyInfoEntry(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'company_email']
        widgets = {            
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Company Name'}),
            'company_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Company Email'}),
            
        }

class DealingYearForm(forms.ModelForm):
    class Meta:
        model = DealingYear
        fields = [ 'dy_session', 'busy_status', 'com_id']
        widgets = {           
            'dy_session': forms.TextInput(attrs={'class': 'form-control'}),
            'busy_status': forms.Select(attrs={'class': 'form-select'}),
            'com_id': forms.Select(attrs={'class': 'form-select'}),
        }



class EmployeeInfoEntry(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'EmpName', 'EmpDesig', 'EmpMobile', 'EmpEmail',
            'EmpBirthDate', 'EmpJoininghDate', 'EmpPicture','EmpComId'
        ]
        exclude = ['EmpId']  # ✅ EmpId ফর্মে দেখাবেন না, কারণ এটি অটো জেনারেটেড

        widgets = {
            'EmpBirthDate': forms.DateInput(attrs={
                'type': 'date', 
                'placeholder': 'Enter BirthDate',
                'class': 'form-control'
            }),
            'EmpJoininghDate': forms.DateInput(attrs={
                'type': 'date', 
                'placeholder': 'Enter JoiningDate',
                'class': 'form-control'
            }),
            'EmpComId': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

    # # Set choices for EmpDiv
    #   self.fields['EmpDiv'] = forms.ChoiceField(
    #     choices=[
    #         ('AC', 'Account (P+M)'),
    #         ('SP', 'Seed Production'),
    #         ('SM', 'Seed Marketing')
    #     ],
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    # ) 



class CatagoryForm(forms.ModelForm):
    class Meta:
        model = Catagory
        fields = ['catagoryid', 'catagoryName', 'catagory_short', 'ComId']
        widgets = {
            'catagoryid': forms.TextInput(attrs={'class': 'form-control'}),
            'catagoryName': forms.TextInput(attrs={'class': 'form-control'}),
            'catagory_short': forms.TextInput(attrs={'class': 'form-control'}),
            'ComId': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Update mode হলে catagory_short readonly করা
            self.fields['catagory_short'].disabled = True

    def clean_catagoryName(self):
        name = self.cleaned_data['catagoryName'].title()  # Capitalized
        qs = Catagory.objects.filter(catagoryName=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)  # exclude current instance
        if qs.exists():
            raise forms.ValidationError("This category name already exists.")
        return name
    

    
from django import forms
from account.models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['employee_id', 'block_id', 'status', 'allowed_app', 'byear', 'com_id']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'allowed_app': forms.Select(attrs={'class': 'form-select'}),
            'employee_id': forms.Select(attrs={'class': 'form-select'}),
            'block_id': forms.Select(attrs={'class': 'form-select'}),
            'byear': forms.Select(attrs={'class': 'form-select'}),
            'com_id': forms.Select(attrs={'class': 'form-select'}),
        }


class HvarietyForm(forms.ModelForm):
    class Meta:
        model = hvariety
        fields = ['hvariety_name', 'contract_company']
        exclude = ['hvariety_id', 'com_id']
        widgets = {           
            'hvariety_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Variety Name'}),
            'contract_company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contract Company'}),
            
        }

    # ✅ Custom validation to prevent duplicate hvariety_name
    def clean_hvariety_name(self):
        name = self.cleaned_data.get('hvariety_name')
        if hvariety.objects.filter(hvariety_name__iexact=name).exists():
            raise forms.ValidationError(f"Variety Name '{name}' already exists.")
        return name    