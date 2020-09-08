from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField, PhoneNumber
# Create your models here.
class User(AbstractUser):
    date_of_birth = models.DateField(blank=False, help_text="Required format YYYY-MM-DD (e.g, 1990-10-25)")
    email = models.EmailField(null=False, blank=False, unique=True)
    mobile_number = PhoneNumberField(blank=False, unique=True, help_text='Example: +61451234567')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'date_of_birth', 'mobile_number',]
    def __str__(self):
        return self.first_name

class Category(models.Model):
    category = models.CharField(blank=False, null=False, max_length=30)
    def __str__(self):
        return self.category

class Item(models.Model):
    name = models.CharField(blank=False, null=False, max_length=64)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, blank=True, related_name='item_categories', default=None)
    price = models.DecimalField(blank=False, max_digits=10, decimal_places=2)
    date_created = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)
    def first_image(self):
        return self.item_images.first()
    def __str__(self):
        return self.name

class ItemImage(models.Model):
    image = models.ImageField(blank=True, upload_to='shopping/uploads')
    caption = models.CharField(blank=True, max_length=100)
    alt_image = models.SlugField(blank=True, max_length=10)
    item = models.ForeignKey(Item, blank=True, null=True, default=None, unique=True, on_delete=models.SET_NULL, related_name='item_images')
    def __str__(self):
        if self.item is not None:
            return self.item.name
        else:
            return f"{self.id}"


class Banner(models.Model):
    image = models.ImageField(blank=False, upload_to='shopping/banner')

class Order(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('R', 'Ready'),
        ('F', 'Fulfilled'),
        ('C', 'Cancelled'),
    )
    customer = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='orders')
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=False, default='P')
    @property
    def price(self):
        price = 0
        for item in self.order_items.all():
            price += item.item.price*item.quantity
        return price
    def __str__(self):
        if self.customer is not None:
            return f"{self.id}: By {self.customer.get_full_name()}"
        else:
            return f"{self.id}"

class ItemOrder(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_orders')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(blank=False)
    def __str__(self):
        if self.order.customer:
            return f"{self.id}: {self.order.customer.get_full_name()}"
        else:
            return f"{self.id}"

class SiteMap(models.Model):
    pass

class AboutUs(models.Model):
    pass
