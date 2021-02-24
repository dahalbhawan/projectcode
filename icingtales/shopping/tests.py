from django.test import TestCase
from shopping.models import *
# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(id=1,
                            first_name="Jacob",
                            email="jacob@gmail.com",
                            gender='Male',
                            password="artofwar",
                            date_of_birth="1994-10-21",
                            mobile_number="+61430738981")
    def test_user_permission(self):
        jacob = User.objects.get(email="jacob@gmail.com")
        self.assertFalse(jacob.is_staff)
        self.assertFalse(jacob.is_superuser)
        self.assertTrue(jacob.is_active)

class CustomItemTestCase(TestCase):
    def setUp(self):
        my_item = Item.objects.create(
            name="MyBirthdayCake",
            description="describe",
            base_price=50,
            )
        my_topping = Topping.objects.create(
            name="Raspberry",
            surcharge=10,
        )
        my_flavor = Flavor.objects.create(
            name="Chocolate",
            surcharge=5,
        )
        CustomItem.objects.create(
            id=1,
            base_item=my_item,
            topping=my_topping,
            flavor=my_flavor,
            size="Medium",
        )
        CustomItem.objects.create(id=2,base_item=my_item)
        CustomItem.objects.create(
            id=3,
            base_item=my_item,
            topping=my_topping,
            size="Large",
        )
    def test_price(self):
        custom1 = CustomItem.objects.get(id=1)
        custom2 = CustomItem.objects.get(id=2)
        custom3 = CustomItem.objects.get(id=3)
        self.assertTrue(custom1.price==75)
        self.assertTrue(custom2.price==50)
        self.assertTrue(custom3.price==80)

class CartTestCase(TestCase):
    def setUp(self):
        User.objects.create(id=1,
                            first_name="Jacob",
                            email="jacob@gmail.com",
                            gender='Male',
                            password="artofwar",
                            date_of_birth="1994-10-21",
                            mobile_number="+61430738981")
        Cart.objects.create(
            id=1,
            user=User.objects.get(id=1)
        )
        my_item = Item.objects.create(
            name="MyBirthdayCake",
            description="describe",
            base_price=50,
        )
        my_topping = Topping.objects.create(
            name="Raspberry",
            surcharge=10,
        )
        my_flavor = Flavor.objects.create(
            name="Chocolate",
            surcharge=5,
        )
        CustomItem.objects.create(
            id=1,
            base_item=my_item,
            topping=my_topping,
            flavor=my_flavor,
            size="Medium",
        )
        CartItem.objects.create(
            custom_item=CustomItem.objects.get(id=1),
            cart = Cart.objects.get(id=1),
            quantity=2,
        )

    def test_cart(self):
        cart1 = Cart.objects.get(id=1)
        self.assertTrue(cart1.price==150)

class OrderTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(id=1,
                            first_name="Jacob",
                            email="jacob@gmail.com",
                            gender='Male',
                            password="artofwar",
                            date_of_birth="1994-10-21",
                            mobile_number="+61430738981")
        my_order = Order.objects.create(
            id=1,
            customer = user,
        )
        my_item = Item.objects.create(
            id=1,
            name="MyBirthdayCake",
            description="describe",
            base_price=50,
        )
        my_topping = Topping.objects.create(
            name="Raspberry",
            surcharge=10,
        )
        my_flavor = Flavor.objects.create(
            name="Chocolate",
            surcharge=5,
        )
        ItemOrder.objects.create(
            id=1,
            item=my_item,
            topping=my_topping,
            flavor=my_flavor,
            order=my_order,
            size="Large",
            quantity=3,
        )
        ItemOrder.objects.create(
            id=2,
            item=my_item,
            topping=my_topping,
            flavor=my_flavor,
            order=my_order,
            quantity=2,
        )
    def test_order(self):
        item = Item.objects.get(id=1)
        itemorder1 = ItemOrder.objects.get(id=1)
        itemorder2 = ItemOrder.objects.get(id=2)
        order = Order.objects.get(id=1)
        self.assertTrue(item.price==50)
        self.assertTrue(itemorder1.price==85)
        self.assertTrue(itemorder2.price==65)
        self.assertTrue(order.price==385)
