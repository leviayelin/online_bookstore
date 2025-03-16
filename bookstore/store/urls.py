from django.urls import path 
from . import views 
app_name = 'store'

urlpatterns = [
    path('', views.store_views, name="home"),
    path('category/<str:book_category>/', views.categories_views, name="category"),
    path('details/<slug:slug>/<int:id>/', views.details_views, name="details"),
    path('add_to_cart/', views.add_to_cart_views, name="cart"),
    path('reviews/add/', views.add_review_views, name="reviews"),
    path('update/', views.update_views, name="update")
]
