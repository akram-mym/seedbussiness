from django.contrib import admin
from account.models import  BlockName, CommonExp,  HeadExp,Advance, UserProfile
from django.utils.html import format_html


# Admin class for BlockName
class BlockNameAdmin(admin.ModelAdmin):
    list_display = (
        'b_id', 'b_name', 'b_land_Ac', 'PerDecimal', 'b_des', 
        'bso_email', 'state', 'rlpay_day', 'land_update', 
        'division', 'emailst', 'com_id'
    )


class HeadExpAdmin(admin.ModelAdmin):
    list_display = ('head_name', 'head_code')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','employee_id','byear','com_id','status', 'allowed_app','block_id')  # যেগুলো লিস্টে দেখাবে


# Register models with their respective admin classes
admin.site.register(BlockName, BlockNameAdmin)

admin.site.register(HeadExp, HeadExpAdmin)
admin.site.register(UserProfile,UserProfileAdmin)

@admin.register(CommonExp)
class CommonExpAdmin(admin.ModelAdmin):
    list_display = ('e_id', 'e_day', 'esubcode', 'ex_cost', 'ExpdBy',  'dy', 'com_id', 'status', 'rtime', 'image_tag')
    list_filter = ('status', 'e_day', 'dy', 'com_id')
    search_fields = ('esubcode', 'EDescribe', 'ExpdBy__name')
    ordering = ('-rtime',)
    

    def image_tag(self, obj):
        if obj.pic:
            return format_html('<img src="{}" style="height: 50px;" />', obj.pic.url)
        return "No Image"
    image_tag.short_description = 'Picture'

    # Optional: readonly_fields if you want to make fields uneditable in admin
    # readonly_fields = ('rtime',)

    # To show only certain fields in the form view
    fieldsets = (
        ('Expense Info', {
            'fields': ('e_day', 'esubcode', 'ex_cost', 'EDescribe', 'status')
        }),
        ('People & Place', {
            'fields': ('ExpdBy', 'b_id', 'dy', 'com_id')
        }),
        ('System Info', {
            'fields': ('myuser', 'mm', 'rtime', 'pic')
        }),
    )

class AdvanceAdmin(admin.ModelAdmin):
    list_display = ('date','receiver','amount','abrief','target_file','rtime','byear','com_id' )

admin.site.register(Advance,AdvanceAdmin)   