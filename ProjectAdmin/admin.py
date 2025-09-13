
from django.contrib import admin

from ProjectAdmin.models import DealingYear, Employee,Catagory,Company

# Admin class for Company
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('com_id', 'company_name', 'company_email','is_active')



class EmployeeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Employee._meta.fields]
    search_fields = ['EmpName', 'EmpEmail']
    list_filter = ['EmpId']


class DealingYearAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DealingYear._meta.fields
                    if field.name != "some_big_text_field" ]


class CatagoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Catagory._meta.fields
                    if field.name != "some_big_text_field" ]


admin.site.register(Company, CompanyAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(DealingYear, DealingYearAdmin)
admin.site.register(Catagory, CatagoryAdmin)