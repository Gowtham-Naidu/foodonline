from django.urls import path
from . import views

urlpatterns = [
    path('registeruser/', views.registeruser,name='registeruser')
]
