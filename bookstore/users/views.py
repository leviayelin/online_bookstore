from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from accounts.forms import CustomUserChangeForm
from store.models import Cart
from .models import CartItem, Order, OrderHistory
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import json

# checkout_cart = the cart for the user (either found or newly created).
# _ = a value saying True if a new cart was created, or False if it already existed — but you're ignoring it because you don’t need it.
# The underscore (_) just means: "I don't care about this value."
# So the line is really just grabbing or making a cart, and ignoring whether it was new or not.

# users profile views
@login_required(login_url='/accounts/login/')
@csrf_exempt
def user_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    user_cart = CartItem.objects.filter(cart=cart)
    # returns multiple OrderItems - queryset (list)
    user_checkout = Order.objects.filter(user=request.user) 
    #order__in means "find orders where the order is in this list."
    order_history = OrderHistory.objects.filter(order__in=user_checkout).select_related('book', 'order') 
    total = sum(item.subtotal() for item in user_cart)

    # Group order history by order
    orders_with_items = {}
    for item in order_history:
        if item.order.id not in orders_with_items:
            orders_with_items[item.order.id] = {
                'order_id': item.order.id,
                'created_at': item.order.created_at,
                'total_price': item.order.total_price,
                'items':[]
            }
        orders_with_items[item.order.id]['items'].append({
            'title':item.book.title,
            'quantity':item.quantity,
            'price':item.price,
            'subtotal':item.get_total(),
        })

        if request.method == 'POST':

            form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('users:user')
    else:

        form = CustomUserChangeForm()  

    return render(request, 'users/users.html', {
        'form':form,
        'user':request.user,
        'user_cart':user_cart,
        'order_history':orders_with_items.values(),
        'total':total
        })


# update cart item quantity at user cart
@login_required(login_url='/accoutns/login/')
@csrf_exempt
def update_cart_views(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get("item_id")
            new_quantity = int(data.get("quantity"))

            if new_quantity < 1:
                return JsonResponse({"success": False,  "error": "Invalid quantity"})
            
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.quantity = new_quantity
            cart_item.save()

            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            total = sum(item.subtotal() for item in cart_items)

            return JsonResponse({
                "success":True,
                "subtotal": cart_item.subtotal(),
                "total": total,
                "total_quantity": sum(item.quantity for item in cart_items)})
        
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
        
    return JsonResponse({"success": False, "error":"Invalid request"})

# user cart items quantity 
@login_required(login_url='/accoutns/login/')
@csrf_exempt
def cart_quantity_views(request):
    if not request.user.is_authenticated:
        login_url = reverse('accounts:login')
        return JsonResponse({'redirect':login_url}, status=401)
    
    cart = CartItem.objects.filter(cart__user=request.user)
    total_quantity = sum(item.quantity for item in cart)

    return JsonResponse({'total_quantity':total_quantity})


# user checkout button
@login_required(login_url='/accoutns/login/')
@csrf_exempt
def checkout_views(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        # Calculate total price
        total_price = sum(item.subtotal() for item in cart_items)


        if not cart_items.exists():
            return JsonResponse({'success': False, 'error': 'Your cart is empty'})

        # Create a new order
        new_order = Order.objects.create(
            user=request.user,
            total_price=Decimal(total_price),
            is_completed = True
        )

        # Move items from cart to order history
        order_items = []
        for item in cart_items:
            OrderHistory.objects.create(
                order=new_order,
                book=item.book,
                quantity = item.quantity,
                price = item.book.price
            )

            order_items.append({
                'title': item.book.title,
                'quantity': item.quantity,
                'price': item.book.price,
                'subtotal': item.subtotal(),
            })
    
        cart_items.delete()

        return JsonResponse({
            'success':True,
            'message':'Order placed successfully',
            'order_id':new_order.id,
            'order_data': {
                'order_id': new_order.id,
                'created_at': new_order.created_at,
                'total_price': float(new_order.total_price),
                'items': order_items
            }
        })

# clear order history button
@login_required(login_url='/accounts/login/')
@csrf_exempt
def clear_history_views(request):
    if request.method == 'POST':
        user = request.user
        user_orders = Order.objects.filter(user=user)
        OrderHistory.objects.filter(order__in=user_orders).delete()
        user_orders.delete()

    return JsonResponse({'success':True,})   


# delete item button
@login_required(login_url='/accoutns/login/')
@csrf_exempt
def delete_views(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()

        # Recalculate total and quantity after deletion
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        total = sum(item.subtotal() for item in cart_items)
        total_quantity = sum(item.quantity for item in cart_items)

        return JsonResponse({'success': True, 'total': total, 'total_quantity': total_quantity})

# delete all items 
@login_required(login_url='/accoutns/login/')
@csrf_exempt
def delete_all_views(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        CartItem.objects.filter(cart=cart).delete()

        return JsonResponse({'success':True})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})
