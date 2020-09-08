from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from datetime import date
from .models import *
from .analytics.analytics import get_top3_purchases
from shopping.froms import *


# Create your views here.
@user_passes_test(lambda u: not (u.is_superuser or u.is_staff), login_url='/sign-in')
def index_view(request):
    if request.user.is_authenticated:
        return render(request, 'shopping/index.html', {
            'first_name': request.user.get_short_name(),
            'banner': Banner.objects.first().image,
            'most_common_items': get_top3_purchases()

        })
    return render(request, 'shopping/index.html', {
        'banner': Banner.objects.first().image,
        'most_common_items': get_top3_purchases()
    })

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
                                            username=email,
                                            email=email,
                                            mobile_number=mobile_number,
                                            date_of_birth=date_of_birth,
                                            password=password1,
                                            )
            Group.objects.get(name='Customer').user_set.add(user)

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
        'orders': orders,
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
            return HttpResponseRedirect(reverse('shopping:admin'))

    return render(request, 'shopping/addorder.html', {
        'order_form': order_form,
        'item_form': item_form,
    })

@staff_member_required(login_url='/sign-in')
@login_required(login_url='/sign-in')
def users_view(request):
    return render(request, 'shopping/users.html', {
    })

def aboutus_view(request):
    return render(request, 'shopping/aboutus.html')

def sitemap_view(request):
    return render(request, 'shopping/sitemap.html')
