from django import forms

from account.models import BlockName, Company

from .models import Catagory, DealingYear, Employee

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
            'EmpBirthDate', 'EmpJoininghDate', 'EmpDiv',
            'EmpPicture'
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

    # Set choices for EmpDiv
      self.fields['EmpDiv'] = forms.ChoiceField(
        choices=[
            ('AC', 'Account (P+M)'),
            ('SP', 'Seed Production'),
            ('SM', 'Seed Marketing')
        ],
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    
    # Hide EmpComId if it exists
      if 'EmpComId' in self.fields: 
       self.fields['EmpComId'].widget = forms.HiddenInput()
    



class CatagoryForm(forms.ModelForm):
    class Meta:
        model = Catagory
        fields = ['catagoryid', 'catagoryName','catagory_short', 'ComId']
        widgets = {
            'catagoryid': forms.TextInput(attrs={'class': 'form-control'}),
            'catagoryName': forms.TextInput(attrs={'class': 'form-control'}),
            'catagoryshort': forms.TextInput(attrs={'class': 'form-control'}),
            'ComId': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_catagoryName(self):
        name = self.cleaned_data['catagoryName'].title()  # Capitalized
        if Catagory.objects.filter(catagoryName=name).exists():
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
