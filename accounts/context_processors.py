from vendor.models import Vendor

#context processors takes request as a argument and returns a dictionary (so it allow to load the context in all html pages)we should register it in settings.py  

def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor= None
    return dict(vendor=vendor)