from django.shortcuts import render, redirect
from .models import BooksData, AddToCart
from users.models import Cart
from django.db import connection
from django.contrib.auth.decorators import login_required


def store_views(request):
    books = BooksData.objects.all()
    return render(request, 'store/store.html', {'books':books})

@login_required(login_url='/accounts/login/')
def add_to_cart(request, product_id):
    product = BooksData.objects.get(book_id=product_id)
    cart, created = AddToCart.objects.get_or_create(user=request.user)
    cart_item, created = Cart.objects.get_or_create(cart=cart, product_book=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('store:home') 

def details_views(request,slug):
    bookDetails = BooksData.objects.get(slug=slug)
    return render(request, 'store/book_details.html', {'book_details':bookDetails})

   