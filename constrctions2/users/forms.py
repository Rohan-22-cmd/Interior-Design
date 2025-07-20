from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

# Custom User Registration Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Ensure this model is correctly defined in models.py
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'  # Add Bootstrap class for styling


# Custom Login Form
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# Admin User Registration Form
class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Ensure this is the correct model
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
