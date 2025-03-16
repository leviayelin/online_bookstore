from django.db import models 

# user cart items model
class CartItem(models.Model):
    cart = models.ForeignKey('store.Cart', on_delete=models.CASCADE)
    book = models.ForeignKey('store.BooksList', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True)

    def quantityLength(self):
        return len(self.quantity)

    def subtotal(self):
        return self.book.price * self.quantity
    
    
    def __str__(self):
        return f"Cart item - {self.quantity} x {self.book}" 


# user order history -  store the final ordered items
# OrderHistory only tracks the overall order without linking to cart items
class Order(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True , null=True)
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    is_completed = models.BooleanField(default=False)

    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

# user items order - saves the ordered books and their quantities at checkout
#  OrderItem model stores what was ordered — detached from the cart — so cart deletions won’t break the history.
class OrderHistory(models.Model):
    order = models.ForeignKey('Order',related_name="items", on_delete=models.CASCADE)
    book = models.ForeignKey('store.BooksList', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def get_total(self):
        return self.quantity * self.price
    

    def __str__(self):
        return f"{self.quantity} X {self.book.title} (Order {self.order.id})"