from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUser

# Create your models here.
class BooksData(models.Model):
    book_id = models.IntegerField(primary_key=True)
    book_title = models.CharField(max_length=150, db_collation='Hebrew_CI_AS', blank=True, null=True)
    author = models.CharField(max_length=100, db_collation='Hebrew_CI_AS', blank=True, null=True)
    categorie = models.CharField(max_length=100, db_collation='Hebrew_CI_AS', blank=True, null=True)
    images = models.URLField(max_length=500, blank=True, null=True)
    book_description = models.TextField(db_collation='Hebrew_CI_AS', blank=True, null=True)
    published_year = models.IntegerField(blank=True, null=True)
    book_rating = models.PositiveIntegerField(blank=True, null=True)
    book_pages = models.IntegerField(blank=True, null=True)
    book_price = models.IntegerField(default=0, blank=True, null=True)
    slug = models.SlugField(max_length=1000, blank=True, null=True)

    def save(self, *arg, **kwargs):
        if not self.slug:
            self.slug = slugify(self.book_title)
        return super().save(*arg, **kwargs)    

    class Meta:
        db_table = 'books_data'


class AddToCart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart - {self.user.username}"