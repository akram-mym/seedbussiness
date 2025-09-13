from django import forms
from ProjectAdmin.models import Employee,Company
from account.models import  Employee, BlockName, BlockName,CommonExp,  HeadExp,Advance, SubHead, UserProfile  # ✅ Import BlockName from current app





class BlockNameForm(forms.ModelForm):
    class Meta:
        model = BlockName
        fields = '__all__'
        exclude = ['b_id']
        widgets = {            
            'b_name': forms.TextInput(attrs={'class': 'form-control'}),
            'b_land_Ac': forms.NumberInput(attrs={'class': 'form-control'}),
            'PerDecimal': forms.NumberInput(attrs={'class': 'form-control'}),
            'b_des': forms.TextInput(attrs={'class': 'form-control'}),
            'bso_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'state': forms.Select(choices=[('ON', 'ON'), ('OFF', 'OFF')], attrs={'class': 'form-control'}),
            'rlpay_day': forms.TextInput(attrs={'class': 'form-control'}),
            'land_update': forms.NumberInput(attrs={'class': 'form-control'}),
            'division': forms.Select(attrs={'class': 'form-control'}),
            'emailst': forms.EmailInput(attrs={'class': 'form-control'}),
            'com_id': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Filter to only active companies
            self.fields['com_id'].queryset = Company.objects.filter(is_active=True).order_by('Company_name')
        
class BlockNameUpdateForm(forms.ModelForm):
    # কাস্টম ফিল্ড (ফর্মে দেখা যাবে, কিন্তু মডেলে নেই)
    confirm_email = forms.EmailField(label='Confirm BSO Email', max_length=40)

    class Meta:
        model = BlockName
        #fields = '__all__'  # অথবা নির্দিষ্ট ফিল্ড চাইলে লিখুন: ['b_id', 'b_name', 'b_land_Ac', ...]
        fields =['b_name', 'b_land_Ac', 'PerDecimal','b_des','bso_email','state','rlpay_day','emailst']
        labels = {
            'b_name'   : 'Block Name',
            'b_land_Ac': 'Land (Acre)',
            'PerDecimal': 'Per decimal Land Rate',
            'b_des'   : 'Block Descriptions',
            'bso_email': 'Block Supervisor Email',
            'state': 'state',
            'rlpay_day': 'Lab Bill Day',
            'emailst': 'Block Email',
        }
        widgets = {
            'b_des': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
            'rlpay_day': forms.Select(choices=[
                ('Sunday', 'Sunday'),
                ('Monday', 'Monday'),
                ('Tuesday', 'Tuesday'),
                ('Wednesday', 'Wednesday'),
                ('Thusday', 'Thusday'),
                ('Saturday', 'Saturday'),
                # প্রয়োজন অনুসারে আরও দিন যুক্ত করুন
            ]),
            'state': forms.Select(choices=[
                ('ON', 'ON'),
                ('OFF', 'OFF')
            ])
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})



    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('bso_email')
        confirm_email = cleaned_data.get('confirm_email')

        if email and confirm_email and email != confirm_email:
            self.add_error('confirm_email', "BSO ইমেইল মিলছে না।")

        return cleaned_data

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['EmpId']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

class CommonExpForm(forms.ModelForm):
    class Meta:
        model = CommonExp
        fields = [
            'e_day',
            'esubcode',
            'ex_cost',
            'EDescribe',
            'ExpdBy',
            'pic',            
            'status',
          
        ]
        widgets = {
            'e_day': forms.DateInput(attrs={'type': 'date'}),
            # 'rtime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            # 'status': forms.Select(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]),
        }
    def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         self.fields['status'].initial = 'Pending'        
        #  self.fields['myuser'].widget.attrs['readonly'] = True
        #  self.fields['rtime'].widget.attrs['readonly'] = True

class HeadExpForm(forms.ModelForm):
    class Meta:
        model = HeadExp
        fields = ['head_code', 'head_name']

class HeadExpViewForm(forms.ModelForm):
    class Meta:
        model = HeadExp
        fields = ['head_code', 'head_name']

    def __init__(self, *args, **kwargs):
        super(HeadExpViewForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True            



class SubHeadForm(forms.ModelForm):
    class Meta:
        model = SubHead
        fields = ['sub_hcode', 'sub_code', 'subhead_name']
        widgets = {
            'sub_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Sub Code'}),
            'subhead_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subhead Name'}),
            'sub_hcode': forms.Select(attrs={'class': 'form-select'}),
        }

        




class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['employee_id', 'block_id', 'status', 'byear','allowed_app', 'com_id']
        widgets = {
            'employee_id': forms.Select(attrs={'class': 'form-select'}),
            'block_id': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'byear': forms.Select(attrs={'class': 'form-select'}),
            'allowed_app': forms.Select(attrs={'class': 'form-select'}),
            'com_id': forms.Select(attrs={'class': 'form-select'}),
        }

class UserProfileListForm1(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super(UserProfileListForm1, self).__init__(*args, **kwargs)
        
        # ✅ Only show Employees who are not already in UserProfile
        registered_employee_ids = UserProfile.objects.values_list('employee_id', flat=True)
        self.fields['employee_id'].queryset = Employee.objects.exclude(EmpId__in=registered_employee_ids).order_by('EmpName')


class advanceEntryForm(forms.ModelForm):
    class Meta:
        model = Advance
        fields = ['date', 'receiver', 'amount', 'abrief', 'target_file']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select Date'
            }),
            'amount': forms.NumberInput(attrs={
                'placeholder': 'Enter Amount',
                'step': '0.01',
                'class': 'form-control'
            }),
            'abrief': forms.Textarea(attrs={
                'placeholder': 'Enter description (optional)',
                'class': 'form-control',
                'rows': 2
            })
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # receiver dropdown: division='AC' ছাড়া সব BlockName
        # self.fields['receiver'].queryset = BlockName.objects.exclude(division='AC')
        # self.fields['b_id'].queryset = BlockName.objects.filter(division='SP')
        self.fields['receiver'].empty_label = "Select Receiver"
        
        
        
        # সব fields Bootstrap class
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class SubHeadEditForm(forms.ModelForm):
    class Meta:
        model = SubHead
        fields = ['sub_hcode', 'sub_code', 'subhead_name']
        widgets = {
            'sub_hcode': forms.Select(attrs={'class': 'form-select'}),
            'sub_code': forms.TextInput(attrs={'class': 'form-control'}),
            'subhead_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Example: make sub_code read-only in form (optional)
        self.fields['sub_code'].disabled = True