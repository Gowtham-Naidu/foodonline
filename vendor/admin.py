from django.contrib import admin
from vendor.models import Vendor
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomVendorAdmin(UserAdmin):
    
    list_display = ('user','restaurant_name','user_profile','is_approved','created_at')
    list_editable = ('is_approved',)
    ordering = ('is_approved',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()    



admin.site.register(Vendor,CustomVendorAdmin)