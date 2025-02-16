from django.shortcuts import render, redirect, HttpResponse
from .models import BooksData, AddToCart, Category
from users.models import Cart
from django.db import connection
from django.contrib.auth.decorators import login_required

# book store home view 
def store_views(request):
    category = Category.objects.all()
    books = BooksData.objects.all()
    return render(request, 'store/store.html', {'books':books, 'categories':category})

# book category selection & views
def categories_views(request, book_category):
    category = Category.objects.all()
    select_category = Category.objects.get(name=book_category)
    book_category = BooksData.objects.filter(category=select_category)
    return render(request, 'store/categories.html', {'categories':book_category,'category': category, 'title':select_category})

# user add to cart function 
@login_required(login_url='/accounts/login/')
def add_to_cart(request, product_id):
    product = BooksData.objects.get(book_id=product_id)
    cart, created = AddToCart.objects.get_or_create(user=request.user)
    cart_item, created = Cart.objects.get_or_create(cart=cart, product_book=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('store:home') 

# book details home view 
def details_views(request,slug):
    bookDetails = BooksData.objects.get(slug=slug)
    return render(request, 'store/book_details.html', {'book_details':bookDetails})

   