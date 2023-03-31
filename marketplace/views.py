from django.shortcuts import render
from vendor.models import Vendor
from django.shortcuts import render,get_object_or_404
from menu.models import Category,Fooditem
from django.db.models import Prefetch
from django.http import HttpResponse,JsonResponse
from .models import Cart
from .context_processors import get_cart_counter
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
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    
    context = {
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html',context)

#add to cart
def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            #checking if the food item exists
            try:
                fooditem = Fooditem.objects.get(id=food_id)
                #checking the usre has already added that food item to cart 
                try:
                    chkcart = Cart.objects.get(user=request.user,fooditem=fooditem)
                    chkcart.quantity += 1
                    chkcart.save() 
                    return JsonResponse({'status':'Success','message':'Increased the cart quantity','cart_counter':get_cart_counter(request),'qty':chkcart.quantity})
               #if food item is not added then add now to cart
                except:
                     chkcart = Cart.objects.create(user=request.user,fooditem=fooditem,quantity=1)
                     return JsonResponse({'status':'Success','message':'Added the food item to the cart','cart_counter':get_cart_counter(request),'qty':chkcart.quantity})
            except:
                return JsonResponse({'status':'Failed','message':'This food does not exits!'})
        else:
          return JsonResponse({'status':'Failed','message':'Ivalied request!'})  
    else:
        return JsonResponse({'status':'login_required','message':'PLEASE LOGIN TO CONTINUE!'})
    
#decrease cart
def decrease_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            #checking if the food item exists 
            try:
                fooditem = Fooditem.objects.get(id=food_id)
                #checking the usre has already added that food item to cart
                try:
                    chkcart = Cart.objects.get(user=request.user,fooditem=fooditem)
                    
                    if chkcart.quantity > 1:
                    #if already added then descreas the quantity
                        chkcart.quantity -= 1
                        chkcart.save() 
                    else:
                        chkcart.delete()
                        chkcart.quantity = 0
                    return JsonResponse({'status':'Success','cart_counter':get_cart_counter(request),'qty':chkcart.quantity})
                except:
                     return JsonResponse({'status':'Failed','message':'You do not have this food item in your cart'})
            except:
                return JsonResponse({'status':'Failed','message':'This food does not exits!'})
        else:
          return JsonResponse({'status':'Failed','message':'Ivalied request!'})  
    else:
        return JsonResponse({'status':'login_required','message':'PLEASE LOGIN TO CONTINUE!'})