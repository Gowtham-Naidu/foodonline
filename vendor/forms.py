from django import forms
from .models import Vendor
from accounts.validators import allow_only_images_validator

class VendorForm(forms.ModelForm):
    restaurant_license = forms.ImageField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[allow_only_images_validator]) #to apply css styles in form 
    
    class Meta:
        model = Vendor
        fields = ['restaurant_name','restaurant_license']
        
        