from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', required=True)
    address = forms.CharField(max_length=50, required=True)
    phone_number = forms.CharField(min_length=10, max_length=11, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'name', 'address')

#
# class StaffForm(forms.Form):
#     name = forms.CharField(max_length=30, required=True)
#     email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', required=True)
#     address = forms.CharField(max_length=50, required=True)
#     phone_number = forms.CharField(min_length=10, max_length=11, required=True)
#
#     class Meta:
#
#         fields = ('username', 'email', 'password1', 'password2', 'name', 'address')
