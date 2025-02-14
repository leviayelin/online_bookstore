from django.urls import path 
from . import views 
app_name = 'store'

urlpatterns = [
    path('', views.store_views, name="home"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('<slug:slug>/details/', views.details_views, name="details"),
]
