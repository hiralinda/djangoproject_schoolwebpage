from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    is_teacher = forms.BooleanField(required=False, label='Are you a teacher?')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'is_teacher')
