from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_view, name="user"),
]

