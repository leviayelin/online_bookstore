from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_view, name='user'),
    path('cart_quantity/', views.cart_quantity_views, name='cart_quantity'),
    path('update_cart/', views.update_cart_views, name='cart_quantity'),
    path('checkout/', views.checkout_views, name='checkout'),
    path('clear_history/', views.clear_history_views, name='clear_history'),
    path('delete/', views.delete_views, name='delete'),
    path('delete_all/', views.delete_all_views, name='delete_all'),
]

