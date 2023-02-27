from django.shortcuts import render,get_object_or_404
from .forms import VendorForm
from accounts.forms import UserProfileForm
from django.contrib import messages
from django.shortcuts import redirect

from accounts.models import UserProfile
from .models import Vendor

from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
# Create your views here.


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    
    #to store the data in DB
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            print('inside if')
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'settings updated.')
            return redirect('vprofile')
        else:
            print('inside else')
            print(profile_form.errors)
            print(vendor_form.errors)
    
    profile_from = UserProfileForm(instance=profile)
    vendor_from = VendorForm(instance=vendor)
    
    context = {
        'profile_from': profile_from,
        'vendor_from' : vendor_from,
        'profile': profile,
        'vendor': vendor, 
    }
        
    return render(request,'vendor/vprofile.html',context)