from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm



class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', required=True)
    address = forms.CharField(max_length=50, required=True)
    phone_number = forms.CharField(min_length=10, max_length=11, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'name', 'address')


class MenuForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=150)
    price = forms.CharField(max_length=10)
    type = forms.CharField(max_length=10)
    item_id = forms.CharField(max_length=50)

    class Meta:
        model = ModelForm
        fields = ('name', 'description', 'price', 'type', 'item_id')

    def clean(self, value):
        try:
            return MenuForm.objects.get(pk=value)
        except:
            raise ValidationError

    def getName(self):
        return self.name

    # TODO update valid Form
    def is_valid(self):
        return True




