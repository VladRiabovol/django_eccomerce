from django.db import models
from django.contrib.auth.models import User
from product.models import Product
# Create your models here.


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.title


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(OrderProduct, null=True, blank=True)
    total_price = models.FloatField(blank=True)

    def __str__(self):
        return self.user.username + str(self.id)

    def save(self, *args, **kwargs):
        products = self.products.all()
        self.total_price = sum(item.price * item.quantity for item in products)
        super(ShopCart, self).save(*args, **kwargs)


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    cart = models.OneToOneField(ShopCart, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
