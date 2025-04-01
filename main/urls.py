from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.index,name='index'),
    path('restocking/', views.restocking, name='restocking'),
    path('restocking/<int:aisle_id>/', views.restocking_aisle, name='restocking_aisle'),
    path('inventory_management',views.inventory_management,name='inventory_management')
]