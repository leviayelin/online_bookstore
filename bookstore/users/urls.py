from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_view, name='user'),
    path('delete/<int:item_id>/', views.delete_item, name='delete'),
]

