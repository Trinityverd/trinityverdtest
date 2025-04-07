from django.urls import path

from . import views

urlpatterns = [
    path('', views.recruitment, name = 'recruitment'),
    path('recruited-farmers', views.recruited_farmers, name = 'recruited_farmers'),
    path('export-farmers', views.export_farmers, name = 'export_farmers')
]