from django import forms
from .models import CustomUser

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'address',]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['address', 'contact_number']