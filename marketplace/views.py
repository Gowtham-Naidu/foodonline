from django.shortcuts import render
from vendor.models import Vendor
from django.shortcuts import render,get_object_or_404
from menu.models import Category,Fooditem
from django.db.models import Prefetch
# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True,user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors':vendors,
        'vendor_count':vendor_count,
    }
    return render(request, 'marketplace/listings.html',context)

def vendor_detail(request,vendor_slug):
    vendor = get_object_or_404(Vendor,vendor_slug=vendor_slug)
    
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'Fooditem',
            queryset=Fooditem.objects.filter(is_available=True)
        )
    )# to get access of fooditem model and to get foodtitle
    
    context = {
        'vendor':vendor,
        'categories':categories,
    }
    return render(request, 'marketplace/vendor_detail.html',context)