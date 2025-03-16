from django.urls import path
from . import views

urlpatterns = [
    path('', views.seed_distribution, name='seed_distri'),
    path('seed_distributed', views.seed_distributed, name='seed_distributed'),
    path('get-farmer-details/<int:farmer_id>/', views.get_farmer_details, name='get_farmer_details'),
    path('export-farmers', views.export_seed, name = 'export_seed')
]
