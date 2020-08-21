from shopping.models import Category

def categories_processor(request):
    cake_categories = [category.category for category in Category.objects.all()]
    return {'cake_categories': cake_categories}