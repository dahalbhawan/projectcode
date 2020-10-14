from shopping.models import *
from shopping.analytics.analytics import *
def categories_processor(request):
    cake_categories = [category.category for category in Category.objects.all()]
    return {'cake_categories': cake_categories}

def flavors_processor(request):
    cake_flavors = [flavor.name for flavor in Flavor.objects.all()]
    return {'cake_flavors': cake_flavors}
def toppings_processor(request):
    cake_toppings = [topping.name for topping in Topping.objects.all()]
    return {'cake_toppings': cake_toppings}
def flowers_processor(request):
    flowers = [flower.name for flower in Flower.objects.all()]
    return {'flowers': flowers}
def best_sellers_processor(request):
    return {'top4_purchases': get_top4_purchases()}

def new_items_processor(request):
    return {'new_items': get_4_recent_items()}