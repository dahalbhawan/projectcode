from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.models import modelformset_factory
from django.forms import inlineformset_factory

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from crispy_forms.bootstrap import InlineField, FormActions, StrictButton, Div
from crispy_forms.layout import Layout
from crispy_forms import bootstrap, layout

class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        # first call the 'real' __init__()
        super(SignInForm, self).__init__(*args, **kwargs)
        # then do extra stuff:
        self.fields['username'].widget = forms.EmailInput(attrs={'placeholder': 'Email address', 'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
        self.fields['username'].label = ''
        self.fields['password'].label = ''

class RegistrationForm(UserCreationForm):
    # date_of_birth = forms.DateField(help_text="Required format YYYY-MM-DD (e.g, 1990-10-25)", widget=
    #                                  forms.DateInput(attrs={'class': 'datepicker form-control'}))
    # mobile_number = formfields.PhoneNumberField(help_text='Example: +61451234567', widget=forms.TextInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender','date_of_birth', 'email', 'mobile_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = forms.DateInput(attrs={'class': 'datepicker form-control'})
        self.fields['mobile_number'].widget = forms.TextInput()
        self.fields['first_name'].widget.attrs['autofocus'] = True
        self.fields['first_name'].required = True

class ToppingCreationForm(forms.ModelForm):
    class Meta:
        model = Topping
        fields = ['name','surcharge']

class ItemCreationForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'categories', 'available_toppings','available_flavors', 'flower', 'base_price','discounted_price', 'status']

class ImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image','caption','alt_image']

class OrderCreationForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'status',]

class ItemOrderForm(forms.ModelForm):
    class Meta:
        model = ItemOrder
        fields = ['item','topping','flavor','size','quantity']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender','date_of_birth', 'email', 'mobile_number',]
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = forms.DateInput(attrs={'class': 'datepicker form-control'})
        self.fields['mobile_number'].widget = forms.TextInput()
        self.fields['first_name'].widget.attrs['autofocus'] = True
        self.fields['first_name'].required = True

ProfileFormset = inlineformset_factory(User, Profile, fields=('profile_image',), max_num=1, can_delete=False)
ItemFormset = modelformset_factory(
    ItemOrder,
    form=ItemOrderForm,
    can_delete=False,
)
ImageFormset = modelformset_factory(
    ItemImage,
    form=ImageForm,
    can_delete=True,
)

class FlavorForm(forms.ModelForm):
    class Meta:
        model = Flavor
        fields = ['name', 'surcharge']

class ToppingForm(forms.ModelForm):
    class Meta:
        model = Topping
        fields = ['name', 'surcharge']

class FlowerForm(forms.ModelForm):
    class Meta:
        model = Flower
        fields = ['name']



