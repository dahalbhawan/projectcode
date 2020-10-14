import os
from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import modelformset_factory
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.template import Context
from xhtml2pdf import pisa
from xhtml2pdf.config.httpconfig import httpConfig
from django.utils.html import strip_tags
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.core import serializers
from django.http import JsonResponse
from datetime import date
from .models import *
from .analytics.analytics import *
from shopping.froms import *
from shopping.utils import *


# Create your views here.
@user_passes_test(lambda u: not (u.is_superuser or u.is_staff), login_url='/sign-in')
def index_view(request):
    if request.user.is_authenticated:
        return render(request, 'shopping/index.html', {
            'first_name': request.user.get_short_name(),
            'banner': Banner.objects.first().image,
            'items' : Item.objects.all()
        })
    return render(request, 'shopping/index.html', {
        'banner': Banner.objects.first().image,
        'items': Item.objects.all()
    })

@user_passes_test(lambda u: not (u.is_superuser or u.is_staff), login_url='/sign-in')
def register_view(request):
    if request.user.is_authenticated:
        logout(request)
    form = RegistrationForm()
    all_users = User.objects.all()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']
            email = form.cleaned_data['email']
            mobile_number = form.cleaned_data['mobile_number']
            date_of_birth = form.cleaned_data['date_of_birth']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if not password1 == password2:
                return render(request, 'shopping/register.html', {
                    'message': 'Password does not match password confirmation',
                    'form': form
                })
            try:
                user = all_users.get(email=email)
                return render(request, 'shopping/register.html', {
                    'message': 'Account already exists with the email',
                    'form': form
                })
            except User.DoesNotExist:
                pass
            try:
                user = all_users.get(mobile_number=mobile_number)
                return render(request, 'shopping/register.html', {
                    'message': 'Account already exists with the mobile number',
                    'form': form
                })
            except:
                pass

            user = User.objects.create_user(first_name=first_name,
                                            last_name=last_name,
                                            gender=gender,
                                            username=email,
                                            email=email,
                                            mobile_number=mobile_number,
                                            date_of_birth=date_of_birth,
                                            password=password1,
                                            )
            Group.objects.get(name='Customer').user_set.add(user)
            profile = Profile(user=user)
            profile.save()
            user.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return HttpResponseRedirect(reverse('shopping:index'))
        return render(request, 'shopping/register.html', {
            'form': form
        })
    return render(request, 'shopping/register.html', {
        'form': form
    })

def signin_view(request):
    form = SignInForm()
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request=request, email=email, password=password)
            if user is not None:
                if user.is_superuser or user.is_staff:
                    login(request, user)
                    return HttpResponseRedirect(reverse('shopping:admin'))
                else:
                    login(request, user, backend="shopping.EmailAuthenticationBackend.EmailBackend")
                    return HttpResponseRedirect(reverse('shopping:index'))

        return render(request, 'shopping/signin.html', {
            'form': SignInForm(),
            'message': 'Invalid email and/or password.'
        })
    return render(request, 'shopping/signin.html', {
        'form': form
    })

def signout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('shopping:index'))

@staff_member_required(login_url='/sign-in')
@login_required(login_url='/sign-in')
def admin_view(request):
    order_status = dict(Order.STATUS_CHOICES)
    #orders = [[getattr(ins, name) for name in field_names] for ins in model.objects.prefetch_related().all()]
    orders = Order.objects.all()

    return render(request, 'shopping/admin.html', {
        'user': request.user,
        'total_orders': Order.objects.count(),
        'total_orders_today': Order.objects.filter(date_created__gte=date.today()).count(),
        'total_orders_pending': Order.objects.filter(status='P').count(),
        'total_orders_ready': Order.objects.filter(status='R').count(),
        'orders': orders.order_by('-date_created'),
        'order_status': order_status
    })

@staff_member_required(login_url='/sign-in')
@login_required(login_url='/sign-in')
def products_view(request):
    return render(request, 'shopping/products.html', {
        'items': Item.objects.all(),
    })
@staff_member_required(login_url='/sign-in')
@login_required(login_url='/sign-in')
def add_product_view(request):
    form = ItemCreationForm()
    image_form = ImageFormset(queryset=ItemImage.objects.none())
    if request.method == 'POST':
        form = ItemCreationForm(request.POST)
        image_form = ImageFormset(request.POST, request.FILES)
        if form.is_valid() and image_form.is_valid():
            item = form.save()
            for form in image_form:
                image = form.save(commit=False)
                image.item = item
                image.save()
            return HttpResponseRedirect(reverse('shopping:products'))
    return render(request, 'shopping/addproduct.html', {
        'form': form,
        'image_form': image_form
    })
@staff_member_required(login_url='/sign-in')
@login_required(login_url='/sign-in')
def update_product_view(request, id):
    product_instance = get_object_or_404(Item, pk=id)
    form = ItemCreationForm(request.POST or None, instance=product_instance)
    image_set = ItemImage.objects.filter(item=product_instance)
    ImageFormset = modelformset_factory(ItemImage, form=ImageForm, max_num=len(image_set))
    image_form = ImageFormset(request.POST or None, request.FILES or None, queryset=image_set)
    if form.is_valid() and image_form.is_valid():
        form.save()
        for form in image_form:
            form.save()
        return HttpResponseRedirect(reverse('shopping:products'))
    return render(request, 'shopping/updateproduct.html', {
        'item': product_instance,
        'form': form,
        'image_form': image_form
    })

@staff_member_required(login_url='/sign-in')
@login_required(login_url='/sign-in')
def update_order_view(request, id):
    order_instance = get_object_or_404(Order,pk=id)
    order_form = OrderCreationForm(request.POST or None, instance=order_instance)
    item_set = ItemOrder.objects.filter(order=order_instance)
    ItemOrderFormset = modelformset_factory(ItemOrder, form=ItemOrderForm, max_num=len(item_set))
    item_form = ItemOrderFormset(request.POST or None, queryset=item_set)
    if order_form.is_valid() and item_form.is_valid():
        order_form.save()
        for form in item_form:
            form.save()
        send_order_status_change_email(order=get_object_or_404(Order,pk=id))
        return HttpResponseRedirect(reverse('shopping:admin'))
    return render(request, 'shopping/updateorder.html', {
        'order': order_instance,
        'order_form': order_form,
        'item_form': item_form,
    })


@staff_member_required(login_url='/sign-in')
@login_required(login_url='/sign-in')
def add_order_view(request):
    order_form = OrderCreationForm()
    item_form = ItemFormset(queryset=ItemOrder.objects.none())
    if request.method == 'POST':
        order_form = OrderCreationForm(request.POST)
        item_form = ItemFormset(request.POST)
        if order_form.is_valid() and item_form.is_valid():
            order = order_form.save()
            for form in item_form:
                item = form.save(commit=False)
                item.order = order
                item.save()
                form.save_m2m()
            send_order_email(order.customer, order)
            return HttpResponseRedirect(reverse('shopping:admin'))

    return render(request, 'shopping/addorder.html', {
        'order_form': order_form,
        'item_form': item_form,
    })

@user_passes_test(lambda u: not (u.is_superuser or u.is_staff), login_url='/sign-in')
def category_view(request, category):
    if not category.lower() == 'all':
        category_object = Category.objects.get(category=category)
        items = category_object.category_items.all()
    else:
        items = Item.objects.all()
    return render(request, 'shopping/category.html', {
        'category': category,
        'items': items,
    })

@user_passes_test(lambda u: not (u.is_superuser or u.is_staff), login_url='/sign-in')
def flavor_view(request, flavor):
    if not flavor.lower() == 'all':
        flavor_object = Flavor.objects.get(name=flavor)
        items = flavor_object.items_with_flavor.all()
    else:
        items = Item.objects.all()
    return render(request, 'shopping/category.html', {
        'flavor': flavor,
        'items': items,
    })

@user_passes_test(lambda u: not (u.is_superuser or u.is_staff), login_url='/sign-in')
def topping_view(request, topping):
    if not topping.lower() == 'all':
        topping_object = Topping.objects.get(name=topping)
        items = topping_object.items_with_topping.all()
    else:
        items = Item.objects.all()
    return render(request, 'shopping/category.html', {
        'topping': topping,
        'items': items,
    })

@user_passes_test(lambda u: not (u.is_superuser or u.is_staff), login_url='/sign-in')
def flower_view(request, flower):
    if not flower.lower() == 'all':
        flower_object = Flower.objects.get(name=flower)
        items = flower_object.flower_items.all()
    else:
        items = Item.objects.all()
    return render(request, 'shopping/category.html', {
        'flower': flower,
        'items': items,
    })

@user_passes_test(lambda u: not (u.is_superuser or u.is_staff), login_url='/sign-in')
def item_view(request, id):
    item = Item.objects.get(pk=id)
    base_price = item.base_price
    if request.method == 'GET' and request.is_ajax():
        topping = request.GET.get("topping")
        flavor = request.GET.get("flavor")
        size = request.GET.get("size")
        flavor_instance = None
        topping_instance = None
        topping_surcharge = 0
        flavor_surcharge = 0
        size_surcharge = 0
        price = base_price
        if request.GET.get('action') == 'reset':
            price = base_price
        else:
            quantity = int(request.GET.get("quantity"))
            # if flavor == "" and (not topping == ""):
            #     topping_surcharge = float(Topping.objects.get(name=topping).surcharge)
            #     price = float(base_price) + topping_surcharge
            # if topping == "" and (not flavor ==""):
            #     flavor_surcharge = float(Flavor.objects.get(name=flavor).surcharge)
            #     price = float(base_price) + flavor_surcharge
            # if (not flavor == "") and (not topping == ""):
            #     topping_surcharge = float(Topping.objects.get(name=topping).surcharge)
            #     flavor_surcharge = float(Flavor.objects.get(name=flavor).surcharge)
            #     price = float(base_price) + topping_surcharge + flavor_surcharge
            if not flavor == "":
                flavor_instance = Flavor.objects.get(name=flavor)
                flavor_surcharge = flavor_instance.surcharge
            if not topping == "":
                topping_instance = Topping.objects.get(name=topping)
                topping_surcharge = topping_instance.surcharge
            custom_item = CustomItem(base_item=item, topping=topping_instance, flavor=flavor_instance, size=size)
            size_surcharge = custom_item.size_surcharge
            price = custom_item.price*quantity
        return JsonResponse({'price': price,
                            'topping_surcharge': topping_surcharge,
                             'flavor_surcharge': flavor_surcharge,
                             'size_surcharge': size_surcharge
                             },
        status=200)

    return render(request, 'shopping/cake.html', {
        'item': item,
    })

@staff_member_required(login_url='/sign-in')
@login_required(login_url='/sign-in')
def users_view(request):
    return render(request, 'shopping/users.html', {
    })

@login_required
def profile_view(request, id):
    profile = Profile.objects.get(user=User.objects.get(pk=id))
    return render(request,'shopping/profile.html', {
        'profile': profile,
    })
def update_profile_view(request, id):
    user_instance = get_object_or_404(User, pk=id)
    profile_instance = get_object_or_404(Profile, user=user_instance)
    user_update_form = UserUpdateForm(request.POST or None, instance=user_instance)
    profile_update_formset = ProfileFormset(request.POST or None, request.FILES or None, instance=user_instance)
    if user_update_form.is_valid() and profile_update_formset.is_valid():
        user_update_form.save()
        for form in profile_update_formset:
            form.save()
        return HttpResponseRedirect(reverse('shopping:profile', kwargs={'id':id}))
    return render(request, 'shopping/updateprofile.html', {
        'user': user_instance,
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_formset,
    })

def cart_view(request, id):
    user_cart = Cart.objects.filter(user=request.user).first()
    if user_cart:
        cart_items = user_cart.cart_items.all()
    else:
        cart_items = None
    return render(request, 'shopping/cart.html',{
        'cart': user_cart,
        'cart_items': cart_items,
    })

def add_to_cart_view(request, item_id):
    item_to_add = Item.objects.get(pk=item_id)
    user_cart, cart_created = Cart.objects.get_or_create(user=request.user)
    if request.method=='POST' and request.is_ajax():
        topping_name = request.POST.get("topping")
        flavor_name = request.POST.get("flavor")
        size = request.POST.get("size")
        quantity = int(request.POST.get("quantity"))
        if not topping_name == "":
            topping = Topping.objects.get(name=topping_name)
        else:
            topping = None
        if not flavor_name == "":
            flavor = Flavor.objects.get(name=flavor_name)
        else:
            flavor = None

        custom_item, custom_item_created = CustomItem.objects.get_or_create(base_item=item_to_add, topping=topping, flavor=flavor, size=size)
        cart_items = user_cart.cart_items.all()
        custom_items = [cart_item.custom_item for cart_item in cart_items]
        if custom_item in custom_items:
            instance = CartItem.objects.get(custom_item=custom_item, cart=user_cart)
            instance.quantity += quantity
            instance.save()
        else:
            instance = CartItem(custom_item=custom_item, cart=user_cart,quantity=quantity)
            instance.save()
        return JsonResponse({'success':True}, status=200)
    return HttpResponseRedirect(reverse('shopping:cart', kwargs={'id': request.user.id}))

def delete_cart_item_view(request, id):
    cart_item = CartItem.objects.get(pk=id)
    cart_item.delete()
    return HttpResponseRedirect(reverse('shopping:cart', kwargs={'id':request.user.id}))

def empty_cart_view(request, id):
    user = request.user
    user_cart = Cart.objects.get(user=user)
    user_cart.delete()
    return HttpResponseRedirect(reverse('shopping:cart', kwargs={'id':request.user.id}))

def checkout_view(request, id):
    user = request.user
    user_cart = Cart.objects.get(user=user)
    cart_items = user_cart.cart_items.all()
    if request.method == 'POST':
        order = Order(customer=user)
        order.save()
        for cart_item in cart_items:
            item_order = ItemOrder(order=order,
                                   item = cart_item.custom_item.base_item,
                                   topping = cart_item.custom_item.topping,
                                   flavor = cart_item.custom_item.flavor,
                                   size = cart_item.custom_item.size,
                                   quantity = cart_item.quantity
                                   )
            item_order.save()
        return HttpResponseRedirect(reverse('shopping:process_payment', kwargs={'order_id': order.id}))
        # return render(request, 'shopping/cart.html', {
        #     'cart': user_cart,
        #     'cart_items': user_cart.cart_items.all(),
        #     'message': "Order successfully Placed"
        # })
    return HttpResponseRedirect(reverse('shopping:cart', kwargs={'id':request.user.id}))

def purchases_view(request, id):
    order_status = dict(Order.STATUS_CHOICES)
    user = request.user
    user_orders = user.orders.all().order_by('-date_created')
    return render(request, 'shopping/purchases.html', {
        'orders': user_orders,
        'order_status': order_status,
        'profile': Profile.objects.get(user=user)
    })

def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.price,
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'AUD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('shopping:payment_done', kwargs={'order_id': order_id})),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('shopping:payment_cancelled', kwargs={'order_id': order_id})),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'shopping/process_payment.html', {'order': order, 'form': form})

@csrf_exempt
def payment_done(request, order_id):
    user = request.user
    user_cart = Cart.objects.get(user=user)
    user_cart.delete()
    order = Order.objects.get(pk=order_id)
    send_order_email(user,order)
    return render(request, 'shopping/payment_done.html', {
        'order': order,
    })

@csrf_exempt
def payment_canceled(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delete()
    return render(request, 'shopping/payment_cancelled.html')

@user_passes_test(lambda u: not (u.is_superuser or u.is_staff), login_url='/sign-in')
def aboutus_view(request):
    return render(request, 'shopping/aboutus.html')
@user_passes_test(lambda u: not (u.is_superuser or u.is_staff), login_url='/sign-in')
def sitemap_view(request):
    return render(request, 'shopping/sitemap.html')

@user_passes_test(lambda u: not (u.is_superuser or u.is_staff), login_url='/sign-in')
def receipt_view(request, order_id):
    return render(request, 'shopping/receipt.html', {
        'order': Order.objects.get(pk=order_id)
    })

@user_passes_test(lambda u: not (u.is_superuser or u.is_staff), login_url='/sign-in')
def generate_PDF_view(request, order_id):
    data = {'order': Order.objects.get(pk=order_id)}

    template = get_template('shopping/receipt_alone.html')
    html  = template.render(data)

    file = open('test.pdf', "w+b")
    # httpConfig.save_keys('nosslcheck', True)
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
    if pisaStatus.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    file.seek(0)
    pdf = file.read()
    file.close()
    return HttpResponse(pdf, 'application/pdf')

@user_passes_test(lambda u: not (u.is_superuser or u.is_staff), login_url='/sign-in')
def search_view(request):
    if request.method == 'GET':
        keyword = request.GET.get('q')
        items = [item for item in Item.objects.all() if keyword.lower() in item.name.lower()]
        categories = [category for category in Category.objects.all() if keyword.lower() in category.category.lower()]
        flavors = [flavor for flavor in Flavor.objects.all() if keyword.lower() in flavor.name.lower()]
        toppings = [topping for topping in Topping.objects.all() if keyword.lower() in topping.name.lower()]
        flowers = [flower for flower in Flower.objects.all() if keyword.lower() in flower.name.lower()]
        return render(request, 'shopping/search.html', {
            'keyword': keyword,
            'items': items,
            'categories': categories,
            'flavors': flavors,
            'toppings': toppings,
            'flowers': flowers,
        })
    return HttpResponseRedirect(reverse('index'))

@staff_member_required(login_url='/sign-in')
@login_required(login_url='/sign-in')
def toppings_view(request):
    toppings = Topping.objects.all()
    return render(request, 'shopping/toppings.html', {
        'toppings': toppings,
    })

@staff_member_required(login_url='/sign-in')
@login_required(login_url='/sign-in')
def add_topping_view(request):
    form = ToppingForm()
    if request.method == 'POST':
        form = ToppingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('shopping:admin_toppings'))
    return render(request, 'shopping/addtopping.html', {
        'form': form
    })

@staff_member_required(login_url='/sign-in')
@login_required(login_url='/sign-in')
def update_topping_view(request, id):
    topping_instance = get_object_or_404(Topping, pk=id)
    form = ToppingForm(request.POST or None, instance=topping_instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('shopping:admin_toppings'))
    return render(request, 'shopping/updatetopping.html', {
        'topping': topping_instance,
        'form': form,
    })

@staff_member_required(login_url='/sign-in')
@login_required(login_url='/sign-in')
def flavors_view(request):
    flavors = Flavor.objects.all()
    return render(request, 'shopping/flavors.html', {
        'flavors': flavors,
    })

@staff_member_required(login_url='/sign-in')
@login_required(login_url='/sign-in')
def add_flavor_view(request):
    form = FlavorForm()
    if request.method == 'POST':
        form = FlavorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('shopping:admin_flavors'))
    return render(request, 'shopping/addflavor.html', {
        'form': form
    })

@staff_member_required(login_url='/sign-in')
@login_required(login_url='/sign-in')
def update_flavor_view(request, id):
    flavor_instance = get_object_or_404(Flavor, pk=id)
    form = FlavorForm(request.POST or None, instance=flavor_instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('shopping:admin_flavors'))
    return render(request, 'shopping/updateflavor.html', {
        'flavor': flavor_instance,
        'form': form,
    })


@staff_member_required(login_url='/sign-in')
@login_required(login_url='/sign-in')
def flowers_view(request):
    flowers = Flower.objects.all()
    return render(request, 'shopping/flowers.html', {
        'flowers': flowers,
    })

@staff_member_required(login_url='/sign-in')
@login_required(login_url='/sign-in')
def add_flower_view(request):
    form = FlowerForm()
    if request.method == 'POST':
        form = FlowerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('shopping:admin_flowers'))
    return render(request, 'shopping/addflower.html', {
        'form': form
    })

@staff_member_required(login_url='/sign-in')
@login_required(login_url='/sign-in')
def update_flower_view(request, id):
    flower_instance = get_object_or_404(Flower, pk=id)
    form = FlowerForm(request.POST or None, instance=flower_instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('shopping:admin_flowers'))
    return render(request, 'shopping/updateflower.html', {
        'flower': flower_instance,
        'form': form,
    })