from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import forms
# Register your models here.

class CustomUserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = forms.UserCreationForm.Meta.fields + ('email','first_name')