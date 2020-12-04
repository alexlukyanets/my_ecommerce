from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import PhoneNumberField

class UserLoginFrom(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterFrom(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)


class CheckoutForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    phone = PhoneNumberField()
    
    # shipping_address = forms.CharField(required=False)
    #
    # shipping_country = CountryField(blank_label='(select country)').formfield(
    #     required=False,
    #     widget=CountrySelectWidget(attrs={
    #         'class': 'custom-select d-block w-100',
    #     }))
    # shipping_zip = forms.CharField(required=False)
    #
    # billing_address = forms.CharField(required=False)
    # billing_address2 = forms.CharField(required=False)
    # billing_country = CountryField(blank_label='(select country)').formfield(
    #     required=False,
    #     widget=CountrySelectWidget(attrs={
    #         'class': 'custom-select d-block w-100',
    #     }))
    # billing_zip = forms.CharField(required=False)
    #
    # same_billing_address = forms.BooleanField(required=False)
    # set_default_shipping = forms.BooleanField(required=False)
    # use_default_shipping = forms.BooleanField(required=False)
    # set_default_billing = forms.BooleanField(required=False)
    # use_default_billing = forms.BooleanField(required=False)
    #
    # payment_option = forms.ChoiceField(
    #     widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    pass