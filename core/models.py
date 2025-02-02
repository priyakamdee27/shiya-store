from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} {self.id}"


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    userImage = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    def imageURL(self):
        try:
            url = self.userImage.url
        except:
            url = ""
        return url


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    material = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    occasion = models.CharField(max_length=100, null=True, blank=True)
    # image

    def __str__(self):
        return self.name

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def add_to_wishlist(self, product):
        self.products.add(product)

    def remove_from_wishlist(self, product):
        self.products.remove(product)


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        orderitems = self.orderitem_set.all()
        shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, blank=True, null=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.address
