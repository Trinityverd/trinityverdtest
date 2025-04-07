from django.urls import path
from . import views

urlpatterns = [
    path('', views.purchases, name='purchases'),
    path('purchased', views.purchased, name = 'purchased'),
    path('export-purchases', views.export_purchases, name = 'export_purchases')
]