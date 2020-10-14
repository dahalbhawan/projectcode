from django.test import TestCase
from shopping.models import *
# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(first_name="Jacob", email="jacob@gmail.com", )
        User.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')