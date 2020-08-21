from shopping.models import *
from collections import Counter

def get_top3_purchases():
    items = []
    most_common_items = []
    for order in Order.objects.all():
        for item in order.items.all():
            items.append(item)
    most_common_counter = Counter(items).most_common()
    return [item[0] for item in most_common_counter]
