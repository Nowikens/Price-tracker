from .models import UserProfile
from django.contrib.auth.models import User
from django import forms

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['wanted_products', 'accepted_price']


