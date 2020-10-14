from io import BytesIO
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from xhtml2pdf import pisa
from django.conf import settings
from .models import *

def send_order_email(user, order):
    subject = f'Order # {order.id} has been placed'
    main_message = 'your order has been successfully placed'
    context = {'order': order, 'order_status': dict(Order.STATUS_CHOICES), 'main_message': main_message}
    html_message_client = render_to_string('shopping/ordermail.html', context)
    html_message_admin = render_to_string('shopping/ordermailadmin.html', context)
    plain_message_client = strip_tags(html_message_client)
    plain_message_admin = strip_tags(html_message_admin)
    from_email = settings.EMAIL_HOST_USER
    client_email = [user.email]
    admin_list = [user for user in User.objects.all() if user.is_superuser and user.is_staff]
    admin_emails = [user.email for user in admin_list]

    send_mail(subject, plain_message_client, from_email, client_email, html_message=html_message_client)
    send_mail(subject, plain_message_admin, from_email,admin_emails, html_message = html_message_admin)

def send_order_status_change_email(order):
    user = order.customer
    main_message = f'your order has been {dict(Order.STATUS_CHOICES).get(order.status)}'
    subject = f'Order # {order.id} {dict(Order.STATUS_CHOICES).get(order.status)}'
    context = {'order': order, 'order_status': dict(Order.STATUS_CHOICES), 'main_message': main_message}
    html_message_client = render_to_string('shopping/ordermail.html', context)
    plain_message_client = strip_tags(html_message_client)
    from_email = settings.EMAIL_HOST_USER
    client_email = [user.email]
    send_mail(subject, plain_message_client, from_email, client_email, html_message=html_message_client)

