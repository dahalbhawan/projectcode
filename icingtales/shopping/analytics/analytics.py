from shopping.models import *
from collections import Counter
from datetime import datetime

def get_top4_purchases():
    items = {}
    for itemorder in ItemOrder.objects.all():
        items[itemorder.item] = itemorder.quantity
    most_common_counter = Counter(items).most_common(4)
    return [item[0] for item in most_common_counter]
def get_4_recent_items():
    items = Item.objects.all().order_by('-date_created')
    return items[:4]
def get_recommended_items(user_id):
    items = {}
    user_orders = Order.objects.filter(customer=User.objects.get(pk=user_id))
    if len(user_orders) > 0:
        for order in user_orders:
            for itemorder in order.order_items.all():
                if itemorder.item in items.keys():
                    items[itemorder.item] += itemorder.quantity
                else:
                    items[itemorder.item] = itemorder.quantity
    if len(items) == 0:
        return []
    elif len(items) > 4:
        most_common_purchases = Counter(items).most_common(4)
    else:
        most_common_purchases = Counter(items).most_common(len(items))
    return [item[0] for item in most_common_purchases]