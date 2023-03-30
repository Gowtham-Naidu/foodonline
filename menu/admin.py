from django.contrib import admin
from menu.models import Category,Fooditem

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('Category_name',)}
    list_display = ('Category_name','vendor','updated_at')
    search_fields = ('Category_name',)
    


class FooditemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('food_title',)}
    list_display = ('food_title','Category','vendor','price','is_available','updated_at')
    search_fields = ('food_title','Category__Category_name','price')
    list_filter = ('is_available',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Fooditem, FooditemAdmin)