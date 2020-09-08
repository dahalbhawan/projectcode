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
    path('products/add', views.add_product_view, name='addproduct'),
    path('order/add', views.add_order_view, name='addorder')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


