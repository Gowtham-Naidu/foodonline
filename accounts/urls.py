from django.urls import path
from . import views

urlpatterns = [
    path('registeruser/', views.registeruser,name='registeruser'),
    path('registervendor/', views.registervendor,name='registervendor'),
]
