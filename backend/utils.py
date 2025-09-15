from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label='Date of Birth'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'date_of_birth')
