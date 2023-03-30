from django import forms
from .models import Category,Fooditem
from accounts.validators import allow_only_images_validator

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['Category_name','description']
        

class FoodItemForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info w-100'}), validators=[allow_only_images_validator])
    class Meta:
        model = Fooditem
        fields = ['Category','food_title','description','price','image','is_available']