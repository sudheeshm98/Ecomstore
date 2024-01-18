from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    description = models.TextField()
    price = models.FloatField(null=True, blank=True)
    image_url = models.CharField(max_length=2048, blank=True)
    book_available = models.BooleanField()


class Order(models.Model):
    product = models.ForeignKey(Book, max_length=200, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Book)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


class CartItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    def total_price(self):
        return float(self.book.price*self.quantity)