from django.shortcuts import render, redirect
from accounts.forms import CustomUserChangeForm
from store.models import AddToCart
from .models import Cart

# users profile views
def user_view(request):
    cart,created = AddToCart.objects.get_or_create(user=request.user)
    user_cart = Cart.objects.filter(cart=cart)
    total = sum(item.subtotal() for item in user_cart)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:user')
    else:
        form = CustomUserChangeForm()        
    return render(request, 'users/users.html', {'form':form, 'user':request.user, 'total':total, 'cart_item':user_cart})

# delete item button
def delete_item(request, item_id):
    item = Cart.objects.get(id=item_id)
    item.delete()
    return redirect('users:user')
