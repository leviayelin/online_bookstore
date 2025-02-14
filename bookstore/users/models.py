from django.db import models 
from store.models import AddToCart, BooksData


class Cart(models.Model):
    cart = models.ForeignKey(AddToCart, on_delete=models.CASCADE)
    product_book = models.ForeignKey(BooksData, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product_book.book_price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product_book}"