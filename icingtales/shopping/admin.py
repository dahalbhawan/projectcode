from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
#Register your models here.
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'gender',
        'email',
        'mobile_number',
        'date_of_birth',
    )
    filter_horizontal = ('groups', 'user_permissions')

class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'date_created',
        'status',
    )
    filter_horizontal = ('categories',)

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'date_created',
        'status',
    )

admin.site.register(User, UsersAdmin)
admin.site.register(Profile)
admin.site.register(Item, ItemAdmin)
admin.site.register(Flower)
admin.site.register(CustomItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Category)
admin.site.register(Topping)
admin.site.register(Flavor)
admin.site.register(ItemImage)
admin.site.register(Banner)
admin.site.register(ItemOrder)
# admin.site.register(Group, GroupAdmin) #no need as Group is by default registered
