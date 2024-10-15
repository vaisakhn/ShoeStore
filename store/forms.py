from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from store.models import UserProfile,ShippingAddress,Reviews



class SignUpForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mb-3'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mb-3'}))

    class Meta:
        model=User
        fields=['username','email','password1','password2']

        widgets={
            'username':forms.TextInput(attrs={'class':'form-control mb-3'}),
            'email':forms.EmailInput(attrs={'class':'form-control mb-3'})
        }

class SignInForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mb-3'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mb-3'}))





class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'full_name',
            'street_address',
            'address_line_2',
            'city',
            'state',
            'postal_code',
            'country',
            'phone_number',
            'email'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name','class':'form-control'}),
            'street_address': forms.TextInput(attrs={'placeholder': 'Street Address','class':'form-control'}),
            'address_line_2': forms.TextInput(attrs={'placeholder': 'Address Line 2','class':'form-control'}),
            'city': forms.TextInput(attrs={'placeholder': 'City','class':'form-control'}),
            'state': forms.TextInput(attrs={'placeholder': 'State','class':'form-control'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Postal Code','class':'form-control'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country','class':'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number','class':'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email','class':'form-control'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model=Reviews
        fields=['comment','rating']
        widgets={
            'rating':forms.NumberInput(attrs={'class':'w-full border p-3','placeholder':'enter a number in between 1 to 5'}),
            'comment':forms.Textarea(attrs={'class':'w-full border p-3','rows':5})
        }