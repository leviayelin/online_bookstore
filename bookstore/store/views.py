from django.shortcuts import render
from .models import BooksData
from django.db import connection


def store_views(request):
    books = BooksData.objects.all()
    return render(request, 'store/store.html', {'books':books})


def details_views(request,slug):
    bookDetails = BooksData.objects.get(slug=slug)
    return render(request, 'store/book_details.html', {'book_details':bookDetails})

# def get_books_categories():
#     categories = [] 
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT DISTINCT categorie FROM books_data")
#         qr = cursor.fetchall()
#         for c in qr:
#             categories.append(c[0])

#     return categories


# print(get_books_categories())    


