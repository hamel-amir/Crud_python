from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2"]

