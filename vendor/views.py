from django.shortcuts import render,get_object_or_404
from .forms import VendorForm
from accounts.forms import UserProfileForm
from django.contrib import messages
from django.shortcuts import redirect

from accounts.models import UserProfile
from .models import Vendor

from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor

from menu.models import Category,Fooditem

from menu.forms import CategoryForm,FoodItemForm
from django.template.defaultfilters import slugify
# Create your views here.

#helper fun to get vendor or we can write it in utils.py
def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

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

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request,'vendor/menu_builder.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request,pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category,pk=pk)
    fooditems = Fooditem.objects.filter(vendor=vendor,Category= category)
    context = {
        'fooditems': fooditems,
        'category':category,
    }
    return render(request, 'vendor/fooditems_by_category.html',context)

#caterogy CRUD
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['Category_name'] #to get category_name from models
            category = form.save(commit=False) #this form is there but not yet saved 
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('menu_builder')
        
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    context = {
        'form':form,
    }
    return render(request,'vendor/add_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request,pk=None):
    category = get_object_or_404(Category,pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['Category_name'] 
            category = form.save(commit=False)  
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('menu_builder')
        
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)
    context = {
        'form':form,
        'category':category,
    }
    return render(request, 'vendor/edit_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request,pk=None):
    category = get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request, 'Category has deleted successfully')
    return redirect('menu_builder')


#fooditem CRUD
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST,request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title'] #to get category_name from models
            food = form.save(commit=False) #this form is there but not yet saved 
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title)
            form.save()
            messages.success(request, 'Food items added successfully!')
            return redirect('fooditems_by_category',food.Category.id)
        
        else:
            print(form.errors)
    else:
        form = FoodItemForm()
        #MODIFY THE FORM check the category for particular vendor
        form.fields['Category'].queryset = Category.objects.filter(vendor=get_vendor(request))
        
    context = {
        'form':form,
    }
    return render(request, 'vendor/add_food.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request,pk=None):
    food = get_object_or_404(Fooditem,pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST,request.FILES,instance=food)
        if form.is_valid():
            food_title = form.cleaned_data['food_title'] 
            food = form.save(commit=False)  
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title)
            form.save()
            messages.success(request, 'Food Item updated successfully!')
            return redirect('fooditems_by_category',food.Category.id)
        
        else:
            print(form.errors)
    else:
        form = FoodItemForm(instance=food)
        #MODIFY THE FORM check the category for particular vendor
        form.fields['Category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form':form,
        'food':food,
    }
    return render(request, 'vendor/edit_food.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request,pk=None):
    food = get_object_or_404(Fooditem,pk=pk)
    food.delete()
    messages.success(request, 'Food item has deleted successfully')
    return redirect('fooditems_by_category', food.Category.id)