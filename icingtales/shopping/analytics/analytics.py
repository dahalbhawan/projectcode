from shopping.models import *
from collections import Counter

def get_top3_purchases():
    items = {}
    for itemorder in ItemOrder.objects.all():
        items[itemorder.item] = itemorder.quantity
    most_common_counter = Counter(items).most_common(3)
    return [item[0] for item in most_common_counter]
