from django.shortcuts import render, redirect, HttpResponse
from .models import BooksList, Cart, Category, Reviews
from users.models import CartItem
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from .forms import ReviewForm
from django.urls import reverse
import json


# book store home view 
def store_views(request):
    category = Category.objects.all()
    books = BooksList.objects.all()
    return render(request, 'store/store.html', {

        'books':books,
        'categories':category

        })

# book category selection & views
def categories_views(request, book_category):
    category = Category.objects.all()
    select_category = Category.objects.get(name=book_category)
    book_category = BooksList.objects.filter(category=select_category)
    
    return render(request, 'store/categories.html', {
        
        'categories': category,
        'category':book_category,
        'title':select_category

        })

# book details home view 
def details_views(request,slug, id):
    bookDetails = BooksList.objects.get(slug=slug, id=id)
    book_reviews = Reviews.objects.filter(book=bookDetails).order_by('-date')

    return render(request, 'store/book_details.html', {
        
        'book_details':bookDetails,
        'book_reviews':book_reviews

        })

# user add to cart function 
@csrf_exempt
def add_to_cart_views(request):
    
    if not request.user.is_authenticated:
        login_url = reverse('accounts:login')
        return JsonResponse({'redirect':login_url},status=401)

    if request.method == 'POST':
    
        try:

            data = json.loads(request.body)
            book_value = data.get('bookId')

            cart, created = Cart.objects.get_or_create(user=request.user)
            book = BooksList.objects.get(id=book_value)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book) 

            if not created:
                cart_item.quantity += 1
                cart_item.save()

            return JsonResponse({'success':True, 'quantity':cart_item.quantity}) 
    
        except BooksList.DoesNotExist:
            return JsonResponse({'error':'Book not found'}, status=405)
        
        except Exception as e:
            print("Error:", str(e)) 
            return JsonResponse({'error':str(e)}, status=500)
            
    return JsonResponse({'error':'Invalid request method'}, status=405)


# user add review section
@login_required(login_url='/accounts/login/')
@csrf_exempt
def add_review_views(request):

    if not request.user.is_authenticated:
        login_url = reverse('accounts:login')
        return JsonResponse({'redirect':login_url}, status=401)
    
    if request.method == 'POST':

        try:

            review = json.loads(request.body)
            book_id = review.get('book_id')
            comment_title = review.get('review_title')
            comment = review.get('review_comment')

            book = BooksList.objects.get(id=book_id)

            user_review = Reviews.objects.create(
                user = request.user,
                book = book,
                title = comment_title,
                comment = comment 
            )

            return JsonResponse({
                'success':True,
                'user': user_review.user.username,
                'book': user_review.book.title,
                'title': user_review.title,
                'date':user_review.date,
                'comment': user_review.comment,
                })
        
        except Exception as e:
          return JsonResponse({'success':False, 'error':str(e)})
        
    return JsonResponse({'success':False})    

@login_required(login_url='/accounts/login/')
@csrf_exempt
def update_views(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) # loads the request
            print(data)
            item_id = data.get("item_id")
            new_quantity = int(data.get("quantity"))

            if new_quantity < 1:
                return JsonResponse({"success":False, "error":"Invalid quantity"})
            
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.quantity = new_quantity
            cart_item.save()

            return JsonResponse({"success":True})
        
        except Exception as e:

            return JsonResponse({"success": False, "error": str(e)})
        
    return JsonResponse({"success":False, "error":"Invalid request"})    
            
          