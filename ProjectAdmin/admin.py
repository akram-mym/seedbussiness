
from django.contrib import admin

from ProjectAdmin.models import DealingYear, Employee,Catagory

class EmployeeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Employee._meta.fields]
    search_fields = ['EmpName', 'EmpEmail']
    list_filter = ['EmpDiv']


class DealingYearAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DealingYear._meta.fields
                    if field.name != "some_big_text_field" ]


class CatagoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Catagory._meta.fields
                    if field.name != "some_big_text_field" ]



admin.site.register(Employee, EmployeeAdmin)
admin.site.register(DealingYear, DealingYearAdmin)
admin.site.register(Catagory, CatagoryAdmin)