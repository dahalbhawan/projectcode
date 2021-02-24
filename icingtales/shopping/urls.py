from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

app_name = "shopping"
urlpatterns = [
    path('', views.index_view, name='index'),
    path('register', views.register_view, name='register'),
    path('sign-in', views.signin_view, name='signin'),
    path('sign-out', views.signout_view, name='signout'),
    path('admin-panel', views.admin_view, name='admin'),
    path('products', views.products_view, name='products'),
    path('users', views.users_view, name='users'),
    path('aboutus', views.aboutus_view, name='aboutus'),
    path('sitemap', views.sitemap_view, name='sitemap'),
    path('search', views.search_view, name='search'),
    path('products/add', views.add_product_view, name='addproduct'),
    path('products/update/<int:id>', views.update_product_view, name='updateproduct'),
    path('order/add', views.add_order_view, name='addorder'),
    path('order/update/<int:id>', views.update_order_view, name='updateorder'),
    path('category/<str:category>', views.category_view, name="category"),
    path('flavor/<str:flavor>', views.flavor_view, name='flavor'),
    path('topping/<str:topping>', views.topping_view, name='topping'),
    path('flower/<str:flower>', views.flower_view, name='flower'),
    path('item/<int:id>', views.item_view, name="item"),
    path('profile/<int:id>', views.profile_view, name="profile"),
    path('profile/<int:id>/update', views.update_profile_view, name="updateprofile"),
    path('cart/<int:id>', views.cart_view, name="cart"),
    path('add-to-cart/<int:item_id>', views.add_to_cart_view, name='add_to_cart'),
    path('delete-cart-item/<int:id>', views.delete_cart_item_view, name='delete_cart_item'),
    path('empty-cart/<int:id>', views.empty_cart_view, name='empty_cart'),
    path('checkout/<int:id>', views.checkout_view, name='checkout'),
    path('process-payment/<int:order_id>', views.process_payment, name='process_payment'),
    path('payment-done/<int:order_id>', views.payment_done, name='payment_done'),
    path('payment-cancelled/<int:order_id>', views.payment_canceled, name='payment_cancelled'),
    path('purchases/<int:id>', views.purchases_view, name='purchases'),
    path('receipt/<int:order_id>', views.receipt_view, name='receipt'),
    path('receipt/<int:order_id>/pdf', views.generate_PDF_view, name='pdf_receipt'),
    path('toppings', views.toppings_view, name='admin_toppings'),
    path('flavors', views.flavors_view, name='admin_flavors'),
    path('flowers', views.flowers_view, name='admin_flowers'),
    path('toppings/add', views.add_topping_view, name='addtopping'),
    path('flavors/add', views.add_flavor_view, name='addflavor'),
    path('flowers/add', views.add_flower_view, name='addflower'),
    path('toppings/update/<int:id>', views.update_topping_view, name='updatetopping'),
    path('flavors/update/<int:id>', views.update_flavor_view, name='updateflavor'),
    path('flowers/update/<int:id>', views.update_flower_view, name='updateflower'),
    path('admin-panel/order/delete/<int:id>', views.delete_order_view, name='deleteorder'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


