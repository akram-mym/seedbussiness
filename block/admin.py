from django.contrib import admin

from block.models import Person

# Register your models here.
class PersonAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Person._meta.fields
                    if field.name != "some_big_text_field" ]

admin.site.register(Person, PersonAdmin)
