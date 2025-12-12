from django import forms
from django.contrib.auth.forms import UserCreationForm
from userapp.models import User , UserProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['image'] 


