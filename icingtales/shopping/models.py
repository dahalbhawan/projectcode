from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField, PhoneNumber
# Create your models here.
class User(AbstractUser):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    date_of_birth = models.DateField(blank=False, help_text="Required format YYYY-MM-DD (e.g, 1990-10-25)")
    email = models.EmailField(null=False, blank=False, unique=True)
    gender = models.CharField(max_length=10, blank=False, null=False, choices=GENDER_CHOICES, default='Male')
    mobile_number = PhoneNumberField(blank=False, unique=True, help_text='Example: +61451234567')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'date_of_birth', 'mobile_number',]
    def __str__(self):
        return self.first_name

class Profile(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, related_name='user_profile')
    profile_image = models.ImageField(blank=True,null=True,upload_to='shopping/uploads/profile')
    def __str__(self):
        return self.user.get_full_name()

class Category(models.Model):
    category = models.CharField(blank=False, null=False, max_length=30)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    def __str__(self):
        return self.category

class Topping(models.Model):
    name = models.CharField(blank=False, null=False, max_length=20)
    surcharge = models.DecimalField(blank=False, null=False, max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name

class Flavor(models.Model):
    name = models.CharField(blank=False, null=False, max_length=20)
    surcharge = models.DecimalField(blank=False, null=False, max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name

class Flower(models.Model):
    name = models.CharField(blank=False, null=False, max_length=20)
    def __str__(self):
        if self.name:
            return self.name

class Item(models.Model):
    name = models.CharField(blank=False, null=False, max_length=64)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, blank=True, related_name='category_items', default=None)
    available_toppings = models.ManyToManyField(Topping, related_name='items_with_topping')
    available_flavors = models.ManyToManyField(Flavor, related_name='items_with_flavor')
    flower = models.ForeignKey(Flower, blank=True, null=True, default=None, related_name='flower_items', on_delete=models.SET_NULL)
    base_price = models.DecimalField(blank=False, max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    date_created = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=True)

    @property
    def price(self):
        if self.discounted_price:
            return self.discounted_price
        return self.base_price

    def first_image(self):
        return self.item_images.first()

    def __str__(self):
        return self.name

class CustomItem(models.Model):
    base_item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='customizations', blank=False, null=False)
    topping = models.ForeignKey(Topping, blank=True, null=True, related_name='topping_items', on_delete=models.SET_NULL)
    flavor = models.ForeignKey(Flavor, blank=True, null=True, related_name='flavor_items', on_delete=models.SET_NULL)
    size = models.TextField(blank=False, null=False, default='Small',max_length=10)
    @property
    def size_surcharge(self):
        size_surcharge = 0
        if self.size == 'Medium':
            size_surcharge = 20/100*float(self.base_item.price)
        elif self.size == 'Large':
            size_surcharge = 40/100*float(self.base_item.price)
        return size_surcharge

    @property
    def price(self):
        price = self.base_item.price
        if self.topping:
            price += self.topping.surcharge
        if self.flavor:
            price += self.flavor.surcharge
        return float(price)+float(self.size_surcharge)
    def __str__(self):
        return self.base_item.name

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
            price += item.price*item.quantity
        return price
    def __str__(self):
        if self.customer is not None:
            return f"{self.id}: By {self.customer.get_full_name()}"
        else:
            return f"{self.id}"

class ItemOrder(models.Model):
    STATUS_CHOICES = (
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_orders')
    topping = models.ForeignKey(Topping, on_delete=models.SET_NULL, blank=True, null=True)
    flavor = models.ForeignKey(Flavor, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    size = models.TextField(blank=False, null=False, default='Small',max_length=10)
    quantity = models.IntegerField(blank=False)
    def __str__(self):
        if self.order.customer:
            return f"{self.id}: {self.order.customer.get_full_name()}"
        else:
            return f"{self.id}"
    @property
    def price(self):
        price = float(self.item.price)
        if self.size == 'Medium':
            price += 20/100*price
        elif self.size == 'Large':
            price += 40/100*price
        if self.topping:
            price += float(self.topping.surcharge)
        if self.flavor:
            price += float(self.flavor.surcharge)
        return price

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    @property
    def price(self):
        price = 0
        cart_items = self.cart_items.all()
        for cart_item in cart_items:
            price += cart_item.price
        return price

    def __str__(self):
        return self.user.get_full_name()

class CartItem(models.Model):
    custom_item = models.ForeignKey(CustomItem, blank=True, null=True, on_delete=models.CASCADE, related_name="custom_item_carts")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.IntegerField(blank=False, default=0)

    @property
    def price(self):
        if self.custom_item:
            return self.custom_item.price*self.quantity
        else:
            return 0
    def __str__(self):
        return self.cart.user.get_full_name()

class SiteMap(models.Model):
    pass

class AboutUs(models.Model):
    pass
