from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

def validate_username_length(value):
    if not 5 <= len(value) <= 20:
        raise ValidationError('Username must be between 5 and 20 characters.')

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(validators=[validate_username_length])
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "First name")
    last_name = forms.CharField(label = "Last name")