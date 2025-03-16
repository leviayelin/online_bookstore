from django.db import models
from django.utils.text import slugify

# categoty model:
# model for creating categories through the admin
# for sectioning each book by genre

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

# book list model:
# basic book database         

class BooksList(models.Model):
    title = models.CharField(max_length=150, db_collation='Hebrew_CI_AS', blank=True, null=True)
    author = models.CharField(max_length=100, db_collation='Hebrew_CI_AS', blank=True, null=True)
    category = models.ForeignKey('Category', max_length=100, blank=True, null=True, on_delete=models.SET_NULL)
    images = models.URLField(max_length=500, blank=True, null=True)
    description = models.TextField(db_collation='Hebrew_CI_AS', blank=True, null=True)
    published_year = models.IntegerField(blank=True, null=True)
    rating = models.PositiveIntegerField(blank=True, null=True)
    book_pages = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    new_commer = models.BooleanField(default=False, null=True)
    best_seller = models.BooleanField(default=False, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.id:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)    

    def __str__(self):
        return self.title

# adding to cart model:
# a model responsible for connecting the adding 
# of an item to the connected user 

class Cart(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart - {self.user.username}"
    
# book review model:
# a user review model, connected user
# can give a review on a book at the 
# book details page

class Reviews(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    book = models.ForeignKey('BooksList', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return f"Review by - {self.user.username}"        
    
