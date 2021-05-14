from django import forms
from django.core.validators import RegexValidator

from . import models


PAYMENT_CHOICES = (  # first param('S') is a "value", second('Stripe') - "name" !!!!!!!!!!!
    ('Stripe', 'Stripe'),
    ('IPay', 'IPay'),
    ('Cash on delivery', 'Cash on delivery')
)

CITY_CHOICE = (
    ('K', 'Kyiv'),
    ('IF', 'Ivano-Frankivsk'),
    ('L', 'Lviv'),
    ('', 'Choose Your City')
)

DELIVERY_CHOICE = (
    ('NewP', 'New Post'),
    ('UkrP', 'Ukrainian Post')
)


class CheckoutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Andrew'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Kowalski'
    }))
    phone_number = forms.DecimalField(
        error_messages={'incomplete': 'Enter a phone number.'},
        validators=[RegexValidator(
            r'^[0-9]+$', 'Enter a valid phone number.')],
        widget=forms.NumberInput(attrs={'placeholder': '0987654321'})
    )

    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'your_email@gmail.com'
    }))

    city = forms.ChoiceField(required=True,
                             widget=forms.Select(attrs={
                                 'label': 'Select Your City',
                                 'class': 'custom-select d-block w-100'
                             }), choices=CITY_CHOICE)

    delivery = forms.ChoiceField(required=True,
                                 widget=forms.Select(attrs={
                                     'label': 'Delivery type',
                                     'class': 'custom-select d-block w-100'
                                 }), choices=DELIVERY_CHOICE)

    # форма для вибору способу оплати: один з кружочків
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)

